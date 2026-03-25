"""Reporting domain ORM models."""

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from contoso_finance.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Report(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A generated financial report covering a date range."""

    __tablename__ = "reports"

    report_type: Mapped[str] = mapped_column(String(50), nullable=False)
    period: Mapped[str] = mapped_column(String(20), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    data_points: Mapped[list["MetricDataPoint"]] = relationship(
        back_populates="report", cascade="all, delete-orphan", lazy="selectin"
    )


class MetricDataPoint(Base, UUIDPrimaryKeyMixin):
    """A single data point within a report."""

    __tablename__ = "metric_data_points"

    report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reports.id", ondelete="CASCADE"), nullable=False
    )
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False)

    report: Mapped["Report"] = relationship(back_populates="data_points")
