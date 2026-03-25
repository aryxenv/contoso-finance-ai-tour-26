"""FastAPI router for the Payments domain."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from contoso_finance.domains.payments import service
from contoso_finance.domains.payments.schemas import (
    PaymentCreate,
    PaymentListResponse,
    PaymentMethodCreate,
    PaymentMethodResponse,
    PaymentResponse,
    RefundRequest,
)
from contoso_finance.shared.database.session import get_db

router = APIRouter(prefix="/api/payments", tags=["payments"])

_NOT_FOUND = {404: {"description": "Payment not found"}}
_VALIDATION = {400: {"description": "Business rule violation"}}


@router.get("/", response_model=PaymentListResponse, summary="List payments")
async def list_payments(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve a paginated list of all payments."""
    return await service.list_payments(db, page, page_size)


@router.get("/methods", response_model=list[PaymentMethodResponse], summary="List payment methods")
async def list_payment_methods(db: AsyncSession = Depends(get_db)):
    """Retrieve all registered payment methods."""
    return await service.list_payment_methods(db)


@router.post(
    "/methods",
    response_model=PaymentMethodResponse,
    status_code=201,
    summary="Create payment method",
    responses=_VALIDATION,
)
async def create_payment_method(
    data: PaymentMethodCreate,
    db: AsyncSession = Depends(get_db),
):
    """Register a new payment method (e.g. credit card, bank account)."""
    return await service.create_payment_method(db, data)


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
    summary="Get payment",
    responses=_NOT_FOUND,
)
async def get_payment(payment_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific payment by its unique identifier."""
    return await service.get_payment(db, payment_id)


@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=201,
    summary="Process payment",
    responses=_VALIDATION,
)
async def process_payment(
    data: PaymentCreate,
    db: AsyncSession = Depends(get_db),
):
    """Process a new payment against an optional invoice."""
    return await service.process_payment(db, data)


@router.post(
    "/{payment_id}/refund",
    response_model=PaymentResponse,
    summary="Refund payment",
    responses={**_NOT_FOUND, **_VALIDATION},
)
async def refund_payment(
    payment_id: UUID,
    refund: RefundRequest,
    db: AsyncSession = Depends(get_db),
):
    """Refund a completed payment, fully or partially."""
    return await service.refund_payment(db, payment_id, refund)
