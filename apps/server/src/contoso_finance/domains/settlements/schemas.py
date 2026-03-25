"""Pydantic schemas for the settlements domain."""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from contoso_finance.shared.types.common import CurrencyCode, PaginatedResponse


class SettlementItemResponse(BaseModel):
    """Response schema for a single settlement item."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(
        description="Unique identifier for the settlement item.",
        examples=["e4f2c1a8-5b3d-4e7f-9a1c-6d8e2f0b3a4c"],
    )
    payment_id: UUID = Field(
        description="Identifier of the payment included in this settlement.",
        examples=["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
    )
    amount: Decimal = Field(
        description="Gross payment amount before fees are deducted.",
        examples=["1500.00"],
    )
    fee: Decimal = Field(
        description="Processing fee charged for this payment.",
        examples=["37.50"],
    )
    net_amount: Decimal = Field(
        description="Net amount after fees (amount minus fee).",
        examples=["1462.50"],
    )


class SettlementCreate(BaseModel):
    """Request schema for creating a new settlement."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payment_ids": [
                    "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                    "b2c3d4e5-f6a7-8901-bcde-f12345678901",
                ],
                "currency": "USD",
                "settlement_date": "2024-07-15",
            }
        }
    )

    payment_ids: list[UUID] = Field(
        description="List of payment IDs to include in this settlement batch.",
        examples=[
            [
                "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "b2c3d4e5-f6a7-8901-bcde-f12345678901",
            ]
        ],
    )
    currency: CurrencyCode = Field(
        description="ISO 4217 currency code for the settlement.",
        examples=["USD"],
    )
    settlement_date: date = Field(
        description="Target date for the settlement payout.",
        examples=["2024-07-15"],
    )


class SettlementResponse(BaseModel):
    """Response schema for a settlement."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(
        description="Unique identifier for the settlement.",
        examples=["d7a3f1b2-4c5e-6d8f-0a1b-2c3d4e5f6a7b"],
    )
    settlement_number: str = Field(
        description="Human-readable settlement reference number.",
        examples=["STL-2024-0001"],
    )
    status: str = Field(
        description="Current status of the settlement.",
        examples=["pending", "completed"],
    )
    currency: str = Field(
        description="ISO 4217 currency code for the settlement.",
        examples=["USD"],
    )
    items: list[SettlementItemResponse] = Field(
        description="Individual payment items included in this settlement.",
    )
    total_amount: Decimal = Field(
        description="Sum of all item amounts before fees.",
        examples=["4500.00"],
    )
    total_fees: Decimal = Field(
        description="Sum of all processing fees across items.",
        examples=["112.50"],
    )
    net_amount: Decimal = Field(
        description="Total payout amount after all fees are deducted.",
        examples=["4387.50"],
    )
    settlement_date: date = Field(
        description="Date the settlement is scheduled or was completed.",
        examples=["2024-07-15"],
    )
    created_at: datetime = Field(
        description="Timestamp when the settlement record was created.",
        examples=["2024-07-14T10:30:00Z"],
    )
    updated_at: datetime = Field(
        description="Timestamp when the settlement record was last updated.",
        examples=["2024-07-15T08:00:00Z"],
    )


class SettlementListResponse(PaginatedResponse[SettlementResponse]):
    """Paginated list of settlements."""

    pass
