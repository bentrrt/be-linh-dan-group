"""Farming period (growing season) model."""

import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Numeric, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class FarmingPeriod(Base):
    __tablename__ = "farming_periods"

    farming_period_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    farmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("farmers.farmer_id"), nullable=False
    )
    crop_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("crop_types.crop_type_id"), nullable=False
    )
    cultivated_area_m2: Mapped[float | None] = mapped_column(Numeric(15, 2))
    cultivated_boundary_geojson: Mapped[dict | None] = mapped_column(JSONB)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str | None] = mapped_column(Text)
    public_code: Mapped[str | None] = mapped_column(Text, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    farmer: Mapped["Farmer"] = relationship(back_populates="farming_periods")  # noqa: F821
    reports: Mapped[list["Report"]] = relationship(  # noqa: F821
        back_populates="farming_period"
    )
