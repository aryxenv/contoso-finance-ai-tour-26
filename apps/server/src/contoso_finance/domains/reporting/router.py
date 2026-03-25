"""Reporting domain API routes."""

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from contoso_finance.domains.reporting import service
from contoso_finance.domains.reporting.schemas import (
    DashboardMetrics,
    ReportListResponse,
    ReportRequest,
    ReportResponse,
)
from contoso_finance.shared.database.session import get_db

router = APIRouter(prefix="/api/reporting", tags=["reporting"])

_NOT_FOUND = {404: {"description": "Report not found"}}


@router.get("/reports", response_model=ReportListResponse, summary="List reports")
async def list_reports(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
) -> ReportListResponse:
    """Retrieve a paginated list of previously generated reports."""
    return await service.list_reports(db, page, page_size)


@router.get(
    "/reports/{report_id}",
    response_model=ReportResponse,
    summary="Get report",
    responses=_NOT_FOUND,
)
async def get_report(
    report_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ReportResponse:
    """Get a single report by its unique identifier."""
    return await service.get_report(db, report_id)


@router.post(
    "/reports",
    response_model=ReportResponse,
    status_code=201,
    summary="Generate report",
)
async def generate_report(
    data: ReportRequest,
    db: AsyncSession = Depends(get_db),
) -> ReportResponse:
    """Generate a new financial report for the specified period and currency."""
    return await service.generate_report(db, data)


@router.delete(
    "/reports/{report_id}",
    status_code=204,
    summary="Delete report",
    responses=_NOT_FOUND,
)
async def delete_report(
    report_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Permanently delete a generated report."""
    await service.delete_report(db, report_id)


@router.get("/dashboard", response_model=DashboardMetrics, summary="Dashboard metrics")
async def get_dashboard_metrics(
    db: AsyncSession = Depends(get_db),
) -> DashboardMetrics:
    """Get aggregated dashboard metrics including revenue, expenses, and pending items."""
    return await service.get_dashboard_metrics(db)
