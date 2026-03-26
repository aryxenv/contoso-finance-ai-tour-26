"""Business-logic layer for the Payments domain."""

import asyncio
import random
import uuid

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from contoso_finance.config import settings
from contoso_finance.domains.payments import repository
from contoso_finance.domains.payments.schemas import (
    PaymentCreate,
    PaymentMethodCreate,
    RefundRequest,
)
from contoso_finance.shared.database.session import async_session_factory
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


async def create_payment(db: AsyncSession, data: PaymentCreate):
    """Create a payment with status 'pending'. Does NOT process it."""
    payment = await repository.create_payment(db, data)
    return payment


async def initiate_processing(
    db: AsyncSession, payment_id: uuid.UUID, background_tasks: BackgroundTasks
):
    """Transition a pending payment to processing and schedule background completion."""
    payment = await repository.get_payment_by_id(db, payment_id)
    if payment is None:
        raise NotFoundError(f"Payment {payment_id} not found")
    if payment.status != "pending":
        raise DomainError(
            f"Cannot process payment with status '{payment.status}'. "
            "Only pending payments can be processed."
        )

    payment = await repository.update_payment_status(db, payment.id, "processing")
    # Commit now so the background task's separate session can see the row
    await db.commit()
    background_tasks.add_task(_simulate_completion, payment.id)
    return payment


async def _simulate_completion(payment_id: uuid.UUID):
    """Background task: simulate processing delay, then complete or fail."""
    await asyncio.sleep(settings.payment_processing_delay_seconds)

    try:
        async with async_session_factory() as session:
            try:
                if random.random() < settings.payment_failure_rate:
                    await repository.update_payment_status(session, payment_id, "failed")
                else:
                    await repository.update_payment_status(session, payment_id, "completed")
                await session.commit()
            except Exception:
                await session.rollback()
                raise
    except Exception:
        # Background task failures are not propagated — the payment stays in
        # "processing" and can be retried or cleaned up by an operator.
        pass


async def get_payment_status(db: AsyncSession, payment_id: uuid.UUID):
    """Return lightweight status info for polling."""
    payment = await repository.get_payment_status(db, payment_id)
    if payment is None:
        raise NotFoundError(f"Payment {payment_id} not found")
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
