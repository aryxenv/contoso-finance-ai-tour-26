"""Authentication router — API endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from contoso_finance.domains.auth import service
from contoso_finance.domains.auth.dependencies import get_current_user
from contoso_finance.domains.auth.models import User
from contoso_finance.domains.auth.schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserResponse,
    UserUpdateRequest,
)
from contoso_finance.shared.database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Create a new user account with email and password."""
    user = await service.register_user(db, data)
    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Log in",
)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    """Authenticate with email and password, returns an access token."""
    return await service.authenticate_user(db, data)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Return the profile of the authenticated user."""
    return UserResponse.model_validate(current_user)


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
)
async def update_me(
    data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Update the authenticated user's profile (name, password)."""
    user = await service.update_user_profile(db, current_user.id, data)
    return UserResponse.model_validate(user)
