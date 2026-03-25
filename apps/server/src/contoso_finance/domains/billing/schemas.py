"""Pydantic v2 schemas for the billing domain."""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from contoso_finance.shared.types.common import CurrencyCode, PaginatedResponse, Status

# --- Line Item schemas ---


class LineItemCreate(BaseModel):
    """Schema for creating a line item."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "Cloud hosting - Pro plan (monthly)",
                "quantity": 3,
                "unit_price": 149.99,
            }
        }
    )

    description: str = Field(
        description="Human-readable description of the line item.",
        examples=["Cloud hosting - Pro plan (monthly)"],
    )
    quantity: int = Field(
        description="Number of units for this line item. Must be at least 1.",
        examples=[3],
    )
    unit_price: float = Field(
        description="Price per unit in the invoice currency.",
        examples=[149.99],
    )


class LineItemResponse(BaseModel):
    """Schema for line item API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(
        description="Unique identifier for the line item.",
        examples=["b3f1c7a2-8d4e-4f6a-9c2b-1a3e5d7f9b0c"],
    )
    description: str = Field(
        description="Human-readable description of the line item.",
        examples=["Cloud hosting - Pro plan (monthly)"],
    )
    quantity: int = Field(
        description="Number of units for this line item.",
        examples=[3],
    )
    unit_price: Decimal = Field(
        description="Price per unit in the invoice currency.",
        examples=["149.99"],
    )
    total: Decimal = Field(
        description="Computed total for this line item (quantity x unit_price).",
        examples=["449.97"],
    )


# --- Invoice schemas ---


class InvoiceCreate(BaseModel):
    """Schema for creating an invoice."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "customer_name": "Northwind Traders",
                "customer_email": "ap@northwindtraders.com",
                "currency": "USD",
                "line_items": [
                    {
                        "description": "Cloud hosting - Pro plan (monthly)",
                        "quantity": 3,
                        "unit_price": 149.99,
                    },
                    {
                        "description": "Premium support add-on",
                        "quantity": 1,
                        "unit_price": 79.00,
                    },
                ],
                "due_date": "2025-08-15",
            }
        }
    )

    customer_name: str = Field(
        description="Full legal name of the customer being invoiced.",
        examples=["Northwind Traders"],
    )
    customer_email: str = Field(
        description="Email address where the invoice will be sent.",
        examples=["ap@northwindtraders.com"],
    )
    currency: CurrencyCode = Field(
        description="ISO 4217 currency code for the invoice.",
        examples=["USD"],
    )
    line_items: list[LineItemCreate] = Field(
        description="One or more line items that make up the invoice.",
    )
    due_date: date = Field(
        description="Date by which payment is expected (YYYY-MM-DD).",
        examples=["2025-08-15"],
    )


class InvoiceUpdate(BaseModel):
    """Schema for partially updating an invoice."""

    customer_name: str | None = Field(
        default=None,
        description="Updated customer name. Omit to leave unchanged.",
        examples=["Northwind Traders"],
    )
    customer_email: str | None = Field(
        default=None,
        description="Updated customer email. Omit to leave unchanged.",
        examples=["billing@northwindtraders.com"],
    )
    currency: CurrencyCode | None = Field(
        default=None,
        description="Updated ISO 4217 currency code. Omit to leave unchanged.",
        examples=["EUR"],
    )
    line_items: list[LineItemCreate] | None = Field(
        default=None,
        description="Replacement set of line items. Omit to leave unchanged.",
    )
    due_date: date | None = Field(
        default=None,
        description="Updated payment due date. Omit to leave unchanged.",
        examples=["2025-09-30"],
    )


class InvoiceResponse(BaseModel):
    """Schema for invoice API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(
        description="Unique identifier for the invoice.",
        examples=["a1d4e8b2-3c7f-4a9e-b5d6-2f8a0c4e6b1d"],
    )
    invoice_number: str = Field(
        description="Human-readable invoice reference number.",
        examples=["INV-2025-00042"],
    )
    customer_name: str = Field(
        description="Full legal name of the invoiced customer.",
        examples=["Northwind Traders"],
    )
    customer_email: str = Field(
        description="Email address associated with the invoice.",
        examples=["ap@northwindtraders.com"],
    )
    status: Status = Field(
        description="Current status of the invoice.",
        examples=["pending"],
    )
    currency: CurrencyCode = Field(
        description="ISO 4217 currency code for the invoice.",
        examples=["USD"],
    )
    subtotal: Decimal = Field(
        description="Sum of all line item totals before tax.",
        examples=["528.97"],
    )
    tax: Decimal = Field(
        description="Calculated tax amount applied to the subtotal.",
        examples=["47.61"],
    )
    total: Decimal = Field(
        description="Final invoice amount including tax (subtotal + tax).",
        examples=["576.58"],
    )
    due_date: date = Field(
        description="Date by which payment is expected.",
        examples=["2025-08-15"],
    )
    line_items: list[LineItemResponse] = Field(
        description="Itemised list of goods or services on the invoice.",
    )
    created_at: datetime = Field(
        description="Timestamp when the invoice was created.",
        examples=["2025-07-01T10:30:00Z"],
    )
    updated_at: datetime = Field(
        description="Timestamp when the invoice was last modified.",
        examples=["2025-07-02T14:15:00Z"],
    )


class InvoiceListResponse(PaginatedResponse[InvoiceResponse]):
    """Paginated list of invoices."""

    pass
