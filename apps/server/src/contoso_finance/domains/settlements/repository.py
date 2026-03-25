"""Data access layer for the settlements domain."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from contoso_finance.domains.settlements.models import Settlement, SettlementItem


async def get_settlements(
    db: AsyncSession, page: int = 1, page_size: int = 20
) -> tuple[list[Settlement], int]:
    """Return a paginated list of settlements with items eager-loaded."""
    count_result = await db.execute(select(func.count(Settlement.id)))
    total = count_result.scalar_one()

    offset = (page - 1) * page_size
    result = await db.execute(
        select(Settlement)
        .options(selectinload(Settlement.items))
        .order_by(Settlement.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    settlements = list(result.scalars().all())
    return settlements, total


async def get_settlement_by_id(
    db: AsyncSession, settlement_id: uuid.UUID
) -> Settlement | None:
    """Return a single settlement by ID, or None if not found."""
    result = await db.execute(
        select(Settlement)
        .options(selectinload(Settlement.items))
        .where(Settlement.id == settlement_id)
    )
    return result.scalar_one_or_none()


async def create_settlement(
    db: AsyncSession,
    settlement_number: str,
    currency: str,
    settlement_date,
    items_data: list[dict],
    totals: dict,
) -> Settlement:
    """Create a new settlement with its items."""
    settlement = Settlement(
        settlement_number=settlement_number,
        currency=currency,
        settlement_date=settlement_date,
        total_amount=totals["total_amount"],
        total_fees=totals["total_fees"],
        net_amount=totals["net_amount"],
        status="pending",
    )
    db.add(settlement)
    await db.flush()

    for item_data in items_data:
        item = SettlementItem(settlement_id=settlement.id, **item_data)
        db.add(item)

    await db.flush()
    await db.refresh(settlement, attribute_names=["items"])
    return settlement


async def update_settlement_status(
    db: AsyncSession, settlement_id: uuid.UUID, status: str
) -> Settlement | None:
    """Update the status of a settlement."""
    settlement = await get_settlement_by_id(db, settlement_id)
    if settlement is None:
        return None
    settlement.status = status
    await db.flush()
    await db.refresh(settlement, attribute_names=["items"])
    return settlement


async def delete_settlement(db: AsyncSession, settlement_id: uuid.UUID) -> bool:
    """Delete a settlement. Returns True if deleted, False if not found."""
    settlement = await get_settlement_by_id(db, settlement_id)
    if settlement is None:
        return False
    await db.delete(settlement)
    await db.flush()
    return True
