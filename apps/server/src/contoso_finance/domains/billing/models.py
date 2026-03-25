"""SQLAlchemy ORM models for the billing domain."""

import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from contoso_finance.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from contoso_finance.shared.types.common import CurrencyCode, Status


class Invoice(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Invoice entity representing a customer billing document."""

    __tablename__ = "invoices"

    invoice_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[Status] = mapped_column(String(20), default=Status.DRAFT, nullable=False)
    currency: Mapped[CurrencyCode] = mapped_column(String(3), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=2), default=Decimal("0.00"))
    tax: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=2), default=Decimal("0.00"))
    total: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=2), default=Decimal("0.00"))
    due_date: Mapped[date] = mapped_column(Date, nullable=False)

    line_items: Mapped[list["LineItem"]] = relationship(
        "LineItem", back_populates="invoice", cascade="all, delete-orphan", lazy="selectin"
    )


class LineItem(UUIDPrimaryKeyMixin, Base):
    """Individual line item on an invoice."""

    __tablename__ = "line_items"

    invoice_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=2), nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=2), nullable=False)

    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="line_items")
