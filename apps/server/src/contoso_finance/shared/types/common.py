"""Common types, enums, and base schemas used across domains."""

from enum import StrEnum
from typing import Generic, TypeVar

from pydantic import BaseModel, Field


class Status(StrEnum):
    """Generic status enum for domain entities."""

    DRAFT = "draft"
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CurrencyCode(StrEnum):
    """Supported currency codes."""

    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


class SortOrder(StrEnum):
    """Sort direction."""

    ASC = "asc"
    DESC = "desc"


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response wrapper."""

    items: list[T] = Field(description="List of items on the current page")
    total: int = Field(description="Total number of items across all pages", examples=[42])
    page: int = Field(description="Current page number (1-indexed)", examples=[1])
    page_size: int = Field(description="Number of items per page", examples=[20])
    total_pages: int = Field(description="Total number of pages", examples=[3])
