"""Business-logic layer for the Payments domain."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from contoso_finance.domains.payments import repository
from contoso_finance.domains.payments.schemas import (
    PaymentCreate,
    PaymentMethodCreate,
    RefundRequest,
)
from contoso_finance.shared.middleware.error_handler import DomainError, NotFoundError


async def list_payments(db: AsyncSession, page: int = 1, page_size: int = 20) -> dict:
    """Return a paginated list of payments."""
    return await repository.get_payments(db, page, page_size)


async def get_payment(db: AsyncSession, payment_id: uuid.UUID):
    """Return a single payment or raise NotFoundError."""
    payment = await repository.get_payment_by_id(db, payment_id)
    if payment is None:
        raise NotFoundError(f"Payment {payment_id} not found")
    return payment


async def process_payment(db: AsyncSession, data: PaymentCreate):
    """Create and process a payment (simulated)."""
    payment = await repository.create_payment(db, data)
    payment = await repository.update_payment_status(db, payment.id, "processing")
    # Simulate successful processing
    payment = await repository.update_payment_status(db, payment.id, "completed")
    return payment


async def refund_payment(
    db: AsyncSession, payment_id: uuid.UUID, refund: RefundRequest
):
    """Refund a completed payment."""
    payment = await repository.get_payment_by_id(db, payment_id)
    if payment is None:
        raise NotFoundError(f"Payment {payment_id} not found")
    if payment.status != "completed":
        raise DomainError(f"Cannot refund payment with status '{payment.status}'")
    payment = await repository.update_payment_status(db, payment_id, "refunded")
    return payment


async def list_payment_methods(db: AsyncSession):
    """Return all payment methods."""
    return await repository.get_payment_methods(db)


async def create_payment_method(db: AsyncSession, data: PaymentMethodCreate):
    """Create a new payment method."""
    return await repository.create_payment_method(db, data)
