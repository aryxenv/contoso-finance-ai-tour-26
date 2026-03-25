"""Reporting domain repository — database access layer."""

import uuid
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from contoso_finance.domains.reporting.models import MetricDataPoint, Report


async def get_reports(
    db: AsyncSession, page: int = 1, page_size: int = 20
) -> tuple[list[Report], int]:
    """Return a paginated list of reports with their data points."""
    count_result = await db.execute(select(func.count(Report.id)))
    total = count_result.scalar_one()

    offset = (page - 1) * page_size
    result = await db.execute(
        select(Report)
        .options(selectinload(Report.data_points))
        .order_by(Report.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    reports = list(result.scalars().all())
    return reports, total


async def get_report_by_id(db: AsyncSession, report_id: uuid.UUID) -> Report | None:
    """Return a single report by ID, or None."""
    result = await db.execute(
        select(Report)
        .options(selectinload(Report.data_points))
        .where(Report.id == report_id)
    )
    return result.scalar_one_or_none()


async def create_report(
    db: AsyncSession,
    report_type: str,
    period: str,
    currency: str,
    start_date: date,
    end_date: date,
    data_points: list[dict],
) -> Report:
    """Create a new report with associated data points."""
    from datetime import datetime, timezone

    report = Report(
        report_type=report_type,
        period=period,
        currency=currency,
        start_date=start_date,
        end_date=end_date,
        generated_at=datetime.now(timezone.utc),
    )

    for dp in data_points:
        report.data_points.append(
            MetricDataPoint(label=dp["label"], value=dp["value"])
        )

    db.add(report)
    await db.flush()
    return report


async def delete_report(db: AsyncSession, report_id: uuid.UUID) -> bool:
    """Delete a report by ID. Returns True if deleted, False if not found."""
    report = await get_report_by_id(db, report_id)
    if report is None:
        return False
    await db.delete(report)
    await db.flush()
    return True
