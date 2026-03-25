"""FastAPI router for the billing domain."""

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from contoso_finance.domains.billing import service
from contoso_finance.domains.billing.schemas import (
    InvoiceCreate,
    InvoiceListResponse,
    InvoiceResponse,
    InvoiceUpdate,
)
from contoso_finance.shared.database.session import get_db

router = APIRouter(prefix="/api/billing", tags=["billing"])

_NOT_FOUND = {404: {"description": "Invoice not found"}}
_VALIDATION = {400: {"description": "Business rule violation"}}


@router.get("/invoices", response_model=InvoiceListResponse, summary="List invoices")
async def list_invoices(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
) -> InvoiceListResponse:
    """Retrieve a paginated list of all invoices, ordered by creation date."""
    result = await service.list_invoices(db, page, page_size)
    return InvoiceListResponse(**result)


@router.get(
    "/invoices/{invoice_id}",
    response_model=InvoiceResponse,
    summary="Get invoice",
    responses=_NOT_FOUND,
)
async def get_invoice(
    invoice_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> InvoiceResponse:
    """Get a single invoice by its unique identifier."""
    invoice = await service.get_invoice(db, invoice_id)
    return InvoiceResponse.model_validate(invoice)


@router.post(
    "/invoices",
    response_model=InvoiceResponse,
    status_code=201,
    summary="Create invoice",
    responses=_VALIDATION,
)
async def create_invoice(
    data: InvoiceCreate,
    db: AsyncSession = Depends(get_db),
) -> InvoiceResponse:
    """Create a new invoice in DRAFT status. Must include at least one line item."""
    invoice = await service.create_invoice(db, data)
    return InvoiceResponse.model_validate(invoice)


@router.patch(
    "/invoices/{invoice_id}",
    response_model=InvoiceResponse,
    summary="Update invoice",
    responses={**_NOT_FOUND, **_VALIDATION},
)
async def update_invoice(
    invoice_id: uuid.UUID,
    data: InvoiceUpdate,
    db: AsyncSession = Depends(get_db),
) -> InvoiceResponse:
    """Partially update an existing invoice. Only DRAFT invoices can be updated."""
    invoice = await service.update_invoice(db, invoice_id, data)
    return InvoiceResponse.model_validate(invoice)


@router.delete(
    "/invoices/{invoice_id}",
    status_code=204,
    summary="Delete invoice",
    responses=_NOT_FOUND,
)
async def delete_invoice(
    invoice_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Permanently delete an invoice."""
    await service.delete_invoice(db, invoice_id)


@router.post(
    "/invoices/{invoice_id}/send",
    response_model=InvoiceResponse,
    summary="Send invoice",
    responses={**_NOT_FOUND, **_VALIDATION},
)
async def send_invoice(
    invoice_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> InvoiceResponse:
    """Send an invoice to the customer (transitions from DRAFT to PENDING)."""
    invoice = await service.send_invoice(db, invoice_id)
    return InvoiceResponse.model_validate(invoice)


@router.post(
    "/invoices/{invoice_id}/mark-paid",
    response_model=InvoiceResponse,
    summary="Mark invoice paid",
    responses={**_NOT_FOUND, **_VALIDATION},
)
async def mark_invoice_paid(
    invoice_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> InvoiceResponse:
    """Mark an invoice as paid (transitions from PENDING to COMPLETED)."""
    invoice = await service.mark_invoice_paid(db, invoice_id)
    return InvoiceResponse.model_validate(invoice)
