"""Reporting domain Pydantic schemas."""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from contoso_finance.shared.types.common import CurrencyCode, PaginatedResponse


class MetricDataPointResponse(BaseModel):
    """A single data point within a financial report."""

    model_config = ConfigDict(from_attributes=True)

    label: str = Field(
        description="Label describing the metric (e.g., month name, category).",
        examples=["January", "Q1 2024"],
    )
    value: float = Field(
        description="Numeric value of the metric in the report's currency.",
        examples=[125000.50, 48000.00],
    )


class ReportRequest(BaseModel):
    """Request body for generating a new financial report."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "revenue",
                "period": "monthly",
                "currency": "USD",
                "start_date": "2024-01-01",
                "end_date": "2024-06-30",
            }
        }
    )

    type: str = Field(
        description="Type of financial report to generate.",
        examples=["revenue", "expense", "cash_flow"],
    )
    period: str = Field(
        description="Aggregation period for the report data points.",
        examples=["monthly", "quarterly", "yearly"],
    )
    currency: CurrencyCode = Field(
        description="ISO 4217 currency code for all monetary values in the report.",
        examples=["USD"],
    )
    start_date: date = Field(
        description="Start date of the reporting period (inclusive).",
        examples=["2024-01-01"],
    )
    end_date: date = Field(
        description="End date of the reporting period (inclusive).",
        examples=["2024-06-30"],
    )


class ReportResponse(BaseModel):
    """Full representation of a generated financial report."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(
        description="Unique identifier for the report.",
        examples=["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
    )
    report_type: str = Field(
        description="Type of financial report.",
        examples=["revenue", "expense"],
    )
    period: str = Field(
        description="Aggregation period used for the report data points.",
        examples=["monthly", "quarterly"],
    )
    currency: CurrencyCode = Field(
        description="ISO 4217 currency code for all monetary values.",
        examples=["USD"],
    )
    start_date: date = Field(
        description="Start date of the reporting period (inclusive).",
        examples=["2024-01-01"],
    )
    end_date: date = Field(
        description="End date of the reporting period (inclusive).",
        examples=["2024-06-30"],
    )
    data_points: list[MetricDataPointResponse] = Field(
        description="Ordered list of metric data points that make up the report.",
    )
    generated_at: datetime = Field(
        description="Timestamp when the report was generated.",
        examples=["2024-07-01T10:30:00Z"],
    )
    created_at: datetime = Field(
        description="Timestamp when the report record was created.",
        examples=["2024-07-01T10:30:00Z"],
    )
    updated_at: datetime = Field(
        description="Timestamp when the report record was last updated.",
        examples=["2024-07-01T10:30:00Z"],
    )


class DashboardMetrics(BaseModel):
    """Aggregated financial metrics displayed on the reporting dashboard."""

    total_revenue: float = Field(
        description="Total revenue for the period in the specified currency.",
        examples=[1250000.00],
    )
    total_expenses: float = Field(
        description="Total expenses for the period in the specified currency.",
        examples=[980000.00],
    )
    net_income: float = Field(
        description="Net income (total revenue minus total expenses).",
        examples=[270000.00],
    )
    pending_invoices: int = Field(
        description="Number of invoices awaiting payment.",
        examples=[12],
    )
    pending_payments: int = Field(
        description="Number of outgoing payments awaiting processing.",
        examples=[8],
    )
    currency: CurrencyCode = Field(
        description="ISO 4217 currency code for all monetary values.",
        examples=["USD"],
    )
    period: str = Field(
        description="Time period these metrics cover.",
        examples=["monthly", "quarterly"],
    )


class ReportListResponse(PaginatedResponse[ReportResponse]):
    """Paginated list of financial reports."""

    pass
