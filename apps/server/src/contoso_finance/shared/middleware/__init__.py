"""Middleware package — error handling and request processing."""

from contoso_finance.shared.middleware.error_handler import (
    ConflictError,
    DomainError,
    NotFoundError,
    register_error_handlers,
)

__all__ = ["register_error_handlers", "DomainError", "NotFoundError", "ConflictError"]
