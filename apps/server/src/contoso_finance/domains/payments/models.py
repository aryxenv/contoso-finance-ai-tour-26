"""SQLAlchemy ORM models for the Payments domain."""

import uuid

from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from contoso_finance.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


def _generate_reference() -> str:
    return f"PAY-{uuid.uuid4().hex[:8].upper()}"


class PaymentMethod(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A stored payment method (credit card, bank transfer, wire)."""

    __tablename__ = "payment_methods"

    type: Mapped[str] = mapped_column(String, nullable=False)
    last_four: Mapped[str] = mapped_column(String(4), nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    payments: Mapped[list["Payment"]] = relationship(back_populates="payment_method")


class Payment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A financial payment record."""

    __tablename__ = "payments"

    invoice_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending", nullable=False)
    payment_method_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("payment_methods.id"), nullable=False
    )
    reference: Mapped[str] = mapped_column(String, unique=True, default=_generate_reference)

    payment_method: Mapped["PaymentMethod"] = relationship(back_populates="payments")
