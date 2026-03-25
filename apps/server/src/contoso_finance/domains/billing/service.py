"""Business logic layer for the billing domain."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from contoso_finance.domains.billing import repository
from contoso_finance.domains.billing.models import Invoice
from contoso_finance.domains.billing.schemas import InvoiceCreate, InvoiceUpdate
from contoso_finance.shared.middleware.error_handler import DomainError, NotFoundError
from contoso_finance.shared.types.common import Status


async def list_invoices(db: AsyncSession, page: int = 1, page_size: int = 20) -> dict:
    """List invoices with pagination."""
    return await repository.get_invoices(db, page, page_size)


async def get_invoice(db: AsyncSession, invoice_id: uuid.UUID) -> Invoice:
    """Get a single invoice by ID. Raises NotFoundError if not found."""
    invoice = await repository.get_invoice_by_id(db, invoice_id)
    if invoice is None:
        raise NotFoundError(f"Invoice {invoice_id} not found")
    return invoice


async def create_invoice(db: AsyncSession, data: InvoiceCreate) -> Invoice:
    """Create a new invoice with calculated totals."""
    return await repository.create_invoice(db, data)


async def update_invoice(db: AsyncSession, invoice_id: uuid.UUID, data: InvoiceUpdate) -> Invoice:
    """Update an existing invoice. Raises NotFoundError if not found."""
    invoice = await repository.update_invoice(db, invoice_id, data)
    if invoice is None:
        raise NotFoundError(f"Invoice {invoice_id} not found")
    return invoice


async def delete_invoice(db: AsyncSession, invoice_id: uuid.UUID) -> None:
    """Delete an invoice. Raises NotFoundError if not found."""
    deleted = await repository.delete_invoice(db, invoice_id)
    if not deleted:
        raise NotFoundError(f"Invoice {invoice_id} not found")


async def send_invoice(db: AsyncSession, invoice_id: uuid.UUID) -> Invoice:
    """Send an invoice — transitions status from DRAFT to PENDING."""
    invoice = await get_invoice(db, invoice_id)
    if invoice.status != Status.DRAFT:
        raise DomainError(f"Invoice can only be sent from DRAFT status, current status is {invoice.status}")
    invoice.status = Status.PENDING
    await db.flush()
    await db.refresh(invoice)
    return invoice


async def mark_invoice_paid(db: AsyncSession, invoice_id: uuid.UUID) -> Invoice:
    """Mark an invoice as paid — transitions status from PENDING to COMPLETED."""
    invoice = await get_invoice(db, invoice_id)
    if invoice.status != Status.PENDING:
        raise DomainError(f"Invoice can only be marked paid from PENDING status, current status is {invoice.status}")
    invoice.status = Status.COMPLETED
    await db.flush()
    await db.refresh(invoice)
    return invoice
