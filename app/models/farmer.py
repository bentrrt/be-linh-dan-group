"""Farmer, land-plot, and farmer-land-plot link models (FR-02, FR-07)."""

import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Numeric, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Farmer(Base):
    __tablename__ = "farmers"

    farmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    farmer_name: Mapped[str] = mapped_column(Text, nullable=False)
    phone_number: Mapped[str | None] = mapped_column(Text)
    # Stores the URL to the farmer's QR code image (FR-09).
    public_code: Mapped[str | None] = mapped_column(Text, unique=True)
    avatar_url: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    land_plots: Mapped[list["FarmerLandPlot"]] = relationship(back_populates="farmer")
    farming_periods: Mapped[list["FarmingPeriod"]] = relationship(  # noqa: F821
        back_populates="farmer"
    )


class LandPlot(Base):
    __tablename__ = "land_plots"

    land_plot_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    land_plot_name: Mapped[str] = mapped_column(Text, nullable=False)
    address_text: Mapped[str | None] = mapped_column(Text)
    total_area_m2: Mapped[float | None] = mapped_column(Numeric(15, 2))
    boundary_geojson: Mapped[dict | None] = mapped_column(JSONB)
    public_code: Mapped[str | None] = mapped_column(Text, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    farmers: Mapped[list["FarmerLandPlot"]] = relationship(back_populates="land_plot")


class FarmerLandPlot(Base):
    __tablename__ = "farmer_land_plots"

    farmer_land_plot_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    farmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("farmers.farmer_id"), nullable=False
    )
    land_plot_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("land_plots.land_plot_id"), nullable=False
    )
    inactive_date: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    farmer: Mapped["Farmer"] = relationship(back_populates="land_plots")
    land_plot: Mapped["LandPlot"] = relationship(back_populates="farmers")
