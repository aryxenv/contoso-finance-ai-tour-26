"""Reporting domain service — business logic layer."""

import math
import random
import uuid
from datetime import date, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from contoso_finance.domains.reporting import repository
from contoso_finance.domains.reporting.schemas import (
    DashboardMetrics,
    ReportListResponse,
    ReportRequest,
    ReportResponse,
)
from contoso_finance.shared.middleware.error_handler import NotFoundError
from contoso_finance.shared.types.common import CurrencyCode


async def list_reports(
    db: AsyncSession, page: int = 1, page_size: int = 20
) -> ReportListResponse:
    """Return a paginated list of reports."""
    reports, total = await repository.get_reports(db, page, page_size)
    return ReportListResponse(
        items=[ReportResponse.model_validate(r) for r in reports],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=max(1, math.ceil(total / page_size)),
    )


async def get_report(db: AsyncSession, report_id: uuid.UUID) -> ReportResponse:
    """Return a single report or raise NotFoundError."""
    report = await repository.get_report_by_id(db, report_id)
    if report is None:
        raise NotFoundError(f"Report {report_id} not found")
    return ReportResponse.model_validate(report)


def _generate_data_points(period: str, start_date: date, end_date: date) -> list[dict]:
    """Generate placeholder data points for a report."""
    points: list[dict] = []

    if period == "monthly":
        current = start_date.replace(day=1)
        while current <= end_date:
            points.append({"label": current.strftime("%b %Y"), "value": round(random.uniform(1000, 50000), 2)})
            month = current.month % 12 + 1
            year = current.year + (1 if current.month == 12 else 0)
            current = current.replace(year=year, month=month)
    elif period == "quarterly":
        quarter = (start_date.month - 1) // 3 + 1
        year = start_date.year
        while date(year, (quarter - 1) * 3 + 1, 1) <= end_date:
            points.append({"label": f"Q{quarter} {year}", "value": round(random.uniform(5000, 200000), 2)})
            quarter += 1
            if quarter > 4:
                quarter = 1
                year += 1
    elif period == "weekly":
        current = start_date
        week = 1
        while current <= end_date:
            points.append({"label": f"Week {week}", "value": round(random.uniform(500, 15000), 2)})
            current += timedelta(weeks=1)
            week += 1
    elif period == "daily":
        current = start_date
        while current <= end_date:
            points.append({"label": current.isoformat(), "value": round(random.uniform(100, 5000), 2)})
            current += timedelta(days=1)
    else:
        # yearly or fallback
        year = start_date.year
        while year <= end_date.year:
            points.append({"label": str(year), "value": round(random.uniform(50000, 500000), 2)})
            year += 1

    return points


async def generate_report(db: AsyncSession, data: ReportRequest) -> ReportResponse:
    """Generate a new report with placeholder data points."""
    data_points = _generate_data_points(data.period, data.start_date, data.end_date)

    report = await repository.create_report(
        db,
        report_type=data.type,
        period=data.period,
        currency=data.currency.value,
        start_date=data.start_date,
        end_date=data.end_date,
        data_points=data_points,
    )
    return ReportResponse.model_validate(report)


async def get_dashboard_metrics(db: AsyncSession) -> DashboardMetrics:
    """Return placeholder dashboard metrics."""
    return DashboardMetrics(
        total_revenue=125_750.00,
        total_expenses=83_200.00,
        net_income=42_550.00,
        pending_invoices=12,
        pending_payments=5,
        currency=CurrencyCode.USD,
        period="monthly",
    )


async def delete_report(db: AsyncSession, report_id: uuid.UUID) -> None:
    """Delete a report or raise NotFoundError."""
    deleted = await repository.delete_report(db, report_id)
    if not deleted:
        raise NotFoundError(f"Report {report_id} not found")
