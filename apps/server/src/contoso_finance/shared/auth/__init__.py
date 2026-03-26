"""Authentication package — JWT tokens and FastAPI dependencies."""

from contoso_finance.shared.auth.dependencies import get_current_user
from contoso_finance.shared.auth.jwt import create_access_token, verify_token
from contoso_finance.shared.auth.password import (
    hash_password,
    validate_password,
    verify_password,
)

__all__ = [
    "get_current_user",
    "create_access_token",
    "verify_token",
    "hash_password",
    "verify_password",
    "validate_password",
]
