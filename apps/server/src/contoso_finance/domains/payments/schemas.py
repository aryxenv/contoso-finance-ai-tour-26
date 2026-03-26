"""Pydantic v2 schemas for the Payments domain."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from contoso_finance.shared.types.common import CurrencyCode, PaginatedResponse


class PaymentMethodCreate(BaseModel):
    """Schema for creating a new payment method."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "visa",
                "last_four": "4242",
            }
        }
    )

    type: str = Field(
        description="Payment method type (e.g. visa, mastercard, amex, bank_transfer).",
        examples=["visa", "mastercard"],
    )
    last_four: str = Field(
        description="Last four digits of the card or account number.",
        examples=["4242", "1234"],
    )


class PaymentMethodResponse(BaseModel):
    """Schema for returning a payment method."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(
        description="Unique identifier for the payment method.",
        examples=["b3e2c1d4-5f6a-7b8c-9d0e-1f2a3b4c5d6e"],
    )
    type: str = Field(
        description="Payment method type.",
        examples=["visa", "mastercard"],
    )
    last_four: str = Field(
        description="Last four digits of the card or account number.",
        examples=["4242"],
    )
    is_default: bool = Field(
        description="Whether this is the customer's default payment method.",
        examples=[True],
    )


class PaymentCreate(BaseModel):
    """Schema for creating a new payment."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "invoice_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "amount": 1500.00,
                "currency": "USD",
                "payment_method_id": "b3e2c1d4-5f6a-7b8c-9d0e-1f2a3b4c5d6e",
            }
        }
    )

    invoice_id: UUID | None = Field(
        default=None,
        description="ID of the invoice this payment is for. Null for standalone payments.",
        examples=["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
    )
    amount: float = Field(
        description="Payment amount in the specified currency.",
        examples=[1500.00, 249.99],
    )
    currency: CurrencyCode = Field(
        description="ISO 4217 currency code for the payment.",
        examples=["USD"],
    )
    payment_method_id: UUID = Field(
        description="ID of the payment method to charge.",
        examples=["b3e2c1d4-5f6a-7b8c-9d0e-1f2a3b4c5d6e"],
    )


class PaymentResponse(BaseModel):
    """Schema for returning a payment."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(
        description="Unique identifier for the payment.",
        examples=["f47ac10b-58cc-4372-a567-0e02b2c3d479"],
    )
    invoice_id: UUID | None = Field(
        description="ID of the associated invoice, or null for standalone payments.",
        examples=["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
    )
    amount: float = Field(
        description="Payment amount in the specified currency.",
        examples=[1500.00],
    )
    currency: str = Field(
        description="ISO 4217 currency code for the payment.",
        examples=["USD"],
    )
    status: str = Field(
        description="Current payment status (e.g. pending, completed, failed, refunded).",
        examples=["completed", "pending"],
    )
    payment_method: PaymentMethodResponse = Field(
        description="Payment method used for this transaction.",
    )
    reference: str = Field(
        description="Unique payment reference code for tracking.",
        examples=["PAY-20250101-ABC123"],
    )
    created_at: datetime = Field(
        description="Timestamp when the payment was created.",
        examples=["2025-01-15T10:30:00Z"],
    )
    updated_at: datetime = Field(
        description="Timestamp when the payment was last updated.",
        examples=["2025-01-15T10:31:00Z"],
    )


class PaymentStatusResponse(BaseModel):
    """Schema for polling a payment's current processing status."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    reference: str
    updated_at: datetime


class RefundRequest(BaseModel):
    """Schema for requesting a refund."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payment_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "amount": 250.00,
                "reason": "Customer requested refund for duplicate charge.",
            }
        }
    )

    payment_id: UUID = Field(
        description="ID of the original payment to refund.",
        examples=["f47ac10b-58cc-4372-a567-0e02b2c3d479"],
    )
    amount: float | None = Field(
        default=None,
        description="Refund amount. If null, the full payment amount is refunded.",
        examples=[250.00],
    )
    reason: str = Field(
        description="Reason for the refund request.",
        examples=["Customer requested refund for duplicate charge."],
    )


class PaymentListResponse(PaginatedResponse[PaymentResponse]):
    """Paginated list of payments."""

    pass
