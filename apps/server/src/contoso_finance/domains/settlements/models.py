"""SQLAlchemy models for the settlements domain."""

import uuid

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from contoso_finance.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Settlement(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A financial settlement that groups one or more payment items."""

    __tablename__ = "settlements"

    settlement_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    total_fees: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    net_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    settlement_date: Mapped[str] = mapped_column(Date, nullable=False)

    items: Mapped[list["SettlementItem"]] = relationship(
        back_populates="settlement", cascade="all, delete-orphan"
    )

    @staticmethod
    def generate_settlement_number() -> str:
        """Generate a unique settlement number in the format STL-{uuid[:8]}."""
        return f"STL-{uuid.uuid4().hex[:8].upper()}"


class SettlementItem(Base, UUIDPrimaryKeyMixin):
    """A single item within a settlement, referencing a payment."""

    __tablename__ = "settlement_items"

    settlement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("settlements.id", ondelete="CASCADE"), nullable=False
    )
    payment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    fee: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    net_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    settlement: Mapped["Settlement"] = relationship(back_populates="items")
