"""Business logic for the settlements domain."""

import math
import uuid
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from contoso_finance.domains.settlements import repository
from contoso_finance.domains.settlements.models import Settlement
from contoso_finance.domains.settlements.schemas import (
    SettlementCreate,
    SettlementListResponse,
    SettlementResponse,
)
from contoso_finance.shared.middleware.error_handler import DomainError, NotFoundError


async def list_settlements(
    db: AsyncSession, page: int = 1, page_size: int = 20
) -> SettlementListResponse:
    """Return a paginated list of settlements."""
    settlements, total = await repository.get_settlements(db, page, page_size)
    total_pages = max(1, math.ceil(total / page_size))
    return SettlementListResponse(
        items=[SettlementResponse.model_validate(s) for s in settlements],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


async def get_settlement(db: AsyncSession, settlement_id: uuid.UUID) -> SettlementResponse:
    """Return a single settlement or raise NotFoundError."""
    settlement = await repository.get_settlement_by_id(db, settlement_id)
    if settlement is None:
        raise NotFoundError(f"Settlement {settlement_id} not found")
    return SettlementResponse.model_validate(settlement)


async def create_settlement(
    db: AsyncSession, data: SettlementCreate
) -> SettlementResponse:
    """Create a new settlement with placeholder items for each payment ID."""
    settlement_number = Settlement.generate_settlement_number()

    # Placeholder item values
    item_amount = Decimal("100.00")
    item_fee = Decimal("2.50")
    item_net = Decimal("97.50")

    items_data = [
        {
            "payment_id": pid,
            "amount": item_amount,
            "fee": item_fee,
            "net_amount": item_net,
        }
        for pid in data.payment_ids
    ]

    count = len(data.payment_ids)
    totals = {
        "total_amount": item_amount * count,
        "total_fees": item_fee * count,
        "net_amount": item_net * count,
    }

    settlement = await repository.create_settlement(
        db,
        settlement_number=settlement_number,
        currency=data.currency.value,
        settlement_date=data.settlement_date,
        items_data=items_data,
        totals=totals,
    )
    return SettlementResponse.model_validate(settlement)


async def _transition_status(
    db: AsyncSession,
    settlement_id: uuid.UUID,
    required_status: str,
    new_status: str,
) -> SettlementResponse:
    """Validate current status and transition to a new status."""
    settlement = await repository.get_settlement_by_id(db, settlement_id)
    if settlement is None:
        raise NotFoundError(f"Settlement {settlement_id} not found")
    if settlement.status != required_status:
        raise DomainError(
            f"Settlement must be in '{required_status}' status to transition to '{new_status}', "
            f"but is currently '{settlement.status}'"
        )
    updated = await repository.update_settlement_status(db, settlement_id, new_status)
    return SettlementResponse.model_validate(updated)


async def reconcile_settlement(
    db: AsyncSession, settlement_id: uuid.UUID
) -> SettlementResponse:
    """Start reconciliation — requires status 'pending'."""
    return await _transition_status(db, settlement_id, "pending", "reconciling")


async def approve_settlement(
    db: AsyncSession, settlement_id: uuid.UUID
) -> SettlementResponse:
    """Approve a settlement — requires status 'reconciling'."""
    return await _transition_status(db, settlement_id, "reconciling", "approved")


async def complete_settlement(
    db: AsyncSession, settlement_id: uuid.UUID
) -> SettlementResponse:
    """Complete a settlement — requires status 'approved'."""
    return await _transition_status(db, settlement_id, "approved", "completed")
