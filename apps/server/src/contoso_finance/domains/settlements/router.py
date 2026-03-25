"""FastAPI router for the settlements domain."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from contoso_finance.domains.settlements import service
from contoso_finance.domains.settlements.schemas import (
    SettlementCreate,
    SettlementListResponse,
    SettlementResponse,
)
from contoso_finance.shared.database.session import get_db

router = APIRouter(prefix="/api/settlements", tags=["settlements"])

_NOT_FOUND = {404: {"description": "Settlement not found"}}
_VALIDATION = {400: {"description": "Business rule violation"}}


@router.get("/", response_model=SettlementListResponse, summary="List settlements")
async def list_settlements(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
) -> SettlementListResponse:
    """Retrieve a paginated list of all settlements."""
    return await service.list_settlements(db, page, page_size)


@router.get(
    "/{settlement_id}",
    response_model=SettlementResponse,
    summary="Get settlement",
    responses=_NOT_FOUND,
)
async def get_settlement(
    settlement_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> SettlementResponse:
    """Get a single settlement by its unique identifier."""
    return await service.get_settlement(db, settlement_id)


@router.post(
    "/",
    response_model=SettlementResponse,
    status_code=201,
    summary="Create settlement",
    responses=_VALIDATION,
)
async def create_settlement(
    data: SettlementCreate,
    db: AsyncSession = Depends(get_db),
) -> SettlementResponse:
    """Create a new settlement by batching one or more payments together."""
    return await service.create_settlement(db, data)


@router.post(
    "/{settlement_id}/reconcile",
    response_model=SettlementResponse,
    summary="Reconcile settlement",
    responses={**_NOT_FOUND, **_VALIDATION},
)
async def reconcile_settlement(
    settlement_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> SettlementResponse:
    """Start reconciliation for a settlement (validates amounts and fees)."""
    return await service.reconcile_settlement(db, settlement_id)


@router.post(
    "/{settlement_id}/approve",
    response_model=SettlementResponse,
    summary="Approve settlement",
    responses={**_NOT_FOUND, **_VALIDATION},
)
async def approve_settlement(
    settlement_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> SettlementResponse:
    """Approve a reconciled settlement for final processing."""
    return await service.approve_settlement(db, settlement_id)


@router.post(
    "/{settlement_id}/complete",
    response_model=SettlementResponse,
    summary="Complete settlement",
    responses={**_NOT_FOUND, **_VALIDATION},
)
async def complete_settlement(
    settlement_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> SettlementResponse:
    """Mark a settlement as completed (funds transferred)."""
    return await service.complete_settlement(db, settlement_id)


@router.delete(
    "/{settlement_id}",
    status_code=204,
    summary="Delete settlement",
    responses=_NOT_FOUND,
)
async def delete_settlement(
    settlement_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Permanently delete a settlement."""
    from contoso_finance.domains.settlements import repository
    from contoso_finance.shared.middleware.error_handler import NotFoundError

    success = await repository.delete_settlement(db, settlement_id)
    if not success:
        raise NotFoundError(f"Settlement {settlement_id} not found")
