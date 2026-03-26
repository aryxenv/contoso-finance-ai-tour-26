"""Authentication service — business logic layer."""

import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from contoso_finance.domains.auth import repository
from contoso_finance.domains.auth.models import User
from contoso_finance.domains.auth.schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserUpdateRequest,
)
from contoso_finance.shared.auth import (
    create_access_token,
    hash_password,
    validate_password,
    verify_password,
)
from contoso_finance.shared.middleware import ConflictError, DomainError, NotFoundError


async def register_user(db: AsyncSession, data: RegisterRequest) -> User:
    """Register a new user account."""
    try:
        validate_password(data.password)
    except ValueError as exc:
        raise DomainError(str(exc)) from exc

    existing = await repository.get_user_by_email(db, data.email)
    if existing:
        raise ConflictError("A user with this email already exists")

    hashed = hash_password(data.password)
    try:
        return await repository.create_user(
            db,
            email=data.email,
            hashed_password=hashed,
            full_name=data.full_name,
        )
    except IntegrityError as exc:
        raise ConflictError("A user with this email already exists") from exc


async def authenticate_user(db: AsyncSession, data: LoginRequest) -> LoginResponse:
    """Authenticate a user and return an access token."""
    user = await repository.get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise DomainError("Invalid email or password", status_code=401)

    if not user.is_active:
        raise DomainError("Account is disabled", status_code=401)

    token = create_access_token({"sub": str(user.id)})
    return LoginResponse(access_token=token)


async def get_user_profile(db: AsyncSession, user_id: uuid.UUID) -> User:
    """Fetch a user's profile by ID."""
    user = await repository.get_user_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")
    return user


async def update_user_profile(
    db: AsyncSession,
    user_id: uuid.UUID,
    data: UserUpdateRequest,
) -> User:
    """Update a user's profile."""
    user = await repository.get_user_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")

    updates: dict[str, object] = {}

    if data.full_name is not None:
        updates["full_name"] = data.full_name

    if data.password is not None:
        if not data.current_password:
            raise DomainError("Current password is required to set a new password")
        if not verify_password(data.current_password, user.hashed_password):
            raise DomainError("Current password is incorrect")
        try:
            validate_password(data.password)
        except ValueError as exc:
            raise DomainError(str(exc)) from exc
        updates["hashed_password"] = hash_password(data.password)

    if updates:
        user = await repository.update_user(db, user, **updates)

    return user
