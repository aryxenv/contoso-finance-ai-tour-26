"""Authentication package — JWT tokens and FastAPI dependencies."""

from contoso_finance.shared.auth.dependencies import get_current_user
from contoso_finance.shared.auth.jwt import create_access_token, verify_token

__all__ = ["get_current_user", "create_access_token", "verify_token"]
