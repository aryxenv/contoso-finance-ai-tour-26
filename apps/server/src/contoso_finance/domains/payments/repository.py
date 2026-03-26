"""Data-access layer for the Payments domain."""

import math
import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from contoso_finance.domains.payments.models import Payment, PaymentMethod
from contoso_finance.domains.payments.schemas import PaymentCreate, PaymentMethodCreate


async def get_payments(
    db: AsyncSession, page: int = 1, page_size: int = 20
) -> dict:
    """Return a paginated list of payments with eager-loaded payment methods."""
    count_result = await db.execute(select(func.count(Payment.id)))
    total = count_result.scalar_one()

    offset = (page - 1) * page_size
    result = await db.execute(
        select(Payment)
        .options(selectinload(Payment.payment_method))
        .order_by(Payment.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    items = list(result.scalars().all())

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, math.ceil(total / page_size)),
    }


async def get_payment_by_id(db: AsyncSession, payment_id: uuid.UUID) -> Payment | None:
    """Return a single payment by ID, or None."""
    result = await db.execute(
        select(Payment)
        .options(selectinload(Payment.payment_method))
        .where(Payment.id == payment_id)
    )
    return result.scalar_one_or_none()


async def create_payment(db: AsyncSession, data: PaymentCreate) -> Payment:
    """Create a new payment with a generated reference."""
    payment = Payment(
        invoice_id=data.invoice_id,
        amount=data.amount,
        currency=data.currency,
        payment_method_id=data.payment_method_id,
    )
    db.add(payment)
    await db.flush()
    await db.refresh(payment, attribute_names=["payment_method"])
    return payment


async def update_payment_status(
    db: AsyncSession, payment_id: uuid.UUID, status: str
) -> Payment | None:
    """Update the status of a payment."""
    payment = await get_payment_by_id(db, payment_id)
    if payment is None:
        return None
    payment.status = status
    await db.flush()
    # Re-fetch to pick up server-generated updated_at and eager-load relationships
    return await get_payment_by_id(db, payment_id)


async def get_payment_status(db: AsyncSession, payment_id: uuid.UUID) -> Payment | None:
    """Get a payment with only status-relevant fields."""
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    return result.scalar_one_or_none()


async def get_payment_methods(db: AsyncSession) -> list[PaymentMethod]:
    """Return all payment methods."""
    result = await db.execute(select(PaymentMethod).order_by(PaymentMethod.created_at.desc()))
    return list(result.scalars().all())


async def create_payment_method(db: AsyncSession, data: PaymentMethodCreate) -> PaymentMethod:
    """Create a new payment method."""
    method = PaymentMethod(type=data.type, last_four=data.last_four)
    db.add(method)
    await db.flush()
    await db.refresh(method)
    return method
