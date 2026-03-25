"""Data access layer for the billing domain."""

import math
import uuid
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from contoso_finance.domains.billing.models import Invoice, LineItem
from contoso_finance.domains.billing.schemas import InvoiceCreate, InvoiceUpdate


async def get_invoices(db: AsyncSession, page: int = 1, page_size: int = 20) -> dict:
    """Retrieve a paginated list of invoices."""
    count_result = await db.execute(select(func.count(Invoice.id)))
    total = count_result.scalar_one()

    offset = (page - 1) * page_size
    result = await db.execute(
        select(Invoice)
        .options(selectinload(Invoice.line_items))
        .order_by(Invoice.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    invoices = list(result.scalars().all())

    return {
        "items": invoices,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, math.ceil(total / page_size)),
    }


async def get_invoice_by_id(db: AsyncSession, invoice_id: uuid.UUID) -> Invoice | None:
    """Retrieve a single invoice by ID, with line items eagerly loaded."""
    result = await db.execute(
        select(Invoice).options(selectinload(Invoice.line_items)).where(Invoice.id == invoice_id)
    )
    return result.scalar_one_or_none()


async def create_invoice(db: AsyncSession, data: InvoiceCreate) -> Invoice:
    """Create a new invoice with its line items."""
    invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"

    line_items: list[LineItem] = []
    subtotal = Decimal("0.00")
    for item in data.line_items:
        item_total = Decimal(str(item.quantity)) * Decimal(str(item.unit_price))
        line_items.append(
            LineItem(
                description=item.description,
                quantity=item.quantity,
                unit_price=Decimal(str(item.unit_price)),
                total=item_total,
            )
        )
        subtotal += item_total

    tax = (subtotal * Decimal("0.10")).quantize(Decimal("0.01"))
    total = subtotal + tax

    invoice = Invoice(
        invoice_number=invoice_number,
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        currency=data.currency,
        subtotal=subtotal,
        tax=tax,
        total=total,
        due_date=data.due_date,
        line_items=line_items,
    )
    db.add(invoice)
    await db.flush()
    await db.refresh(invoice)
    return invoice


async def update_invoice(db: AsyncSession, invoice_id: uuid.UUID, data: InvoiceUpdate) -> Invoice | None:
    """Update an existing invoice. Returns None if not found."""
    invoice = await get_invoice_by_id(db, invoice_id)
    if invoice is None:
        return None

    update_data = data.model_dump(exclude_unset=True)

    # Handle line items replacement if provided
    if "line_items" in update_data:
        raw_items = update_data.pop("line_items")
        # Remove existing line items
        invoice.line_items.clear()

        subtotal = Decimal("0.00")
        for item in raw_items:
            item_total = Decimal(str(item["quantity"])) * Decimal(str(item["unit_price"]))
            invoice.line_items.append(
                LineItem(
                    description=item["description"],
                    quantity=item["quantity"],
                    unit_price=Decimal(str(item["unit_price"])),
                    total=item_total,
                )
            )
            subtotal += item_total

        invoice.subtotal = subtotal
        invoice.tax = (subtotal * Decimal("0.10")).quantize(Decimal("0.01"))
        invoice.total = invoice.subtotal + invoice.tax

    for field, value in update_data.items():
        setattr(invoice, field, value)

    await db.flush()
    await db.refresh(invoice)
    return invoice


async def delete_invoice(db: AsyncSession, invoice_id: uuid.UUID) -> bool:
    """Delete an invoice by ID. Returns True if deleted, False if not found."""
    invoice = await get_invoice_by_id(db, invoice_id)
    if invoice is None:
        return False
    await db.delete(invoice)
    await db.flush()
    return True
