"""Report models (FR-03/04/05/06/08/10/11): unified report, media, drug applications."""

import enum
import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ReportType(str, enum.Enum):
    """Report kinds matching the `report_type_enum` Postgres type."""

    YIELD = "YIELD"
    FARMING_STAGE = "FARMING_STAGE"
    FARM_VISIT = "FARM_VISIT"


# Bind to the existing named enum type; do not let SQLAlchemy create/drop it.
report_type_enum = ENUM(
    ReportType,
    name="report_type_enum",
    create_type=False,
    values_callable=lambda e: [member.value for member in e],
)


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
        CheckConstraint(
            "gps_lat IS NULL OR gps_lat BETWEEN -90 AND 90",
            name="chk_reports_gps_lat",
        ),
        CheckConstraint(
            "gps_long IS NULL OR gps_long BETWEEN -180 AND 180",
            name="chk_reports_gps_long",
        ),
    )

    report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    farming_period_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("farming_periods.farming_period_id"),
        nullable=False,
    )
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    report_type: Mapped[ReportType] = mapped_column(report_type_enum, nullable=False)
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)
    submitted_mac_address: Mapped[str | None] = mapped_column(Text)
    gps_lat: Mapped[float | None] = mapped_column(Numeric(10, 7))
    gps_long: Mapped[float | None] = mapped_column(Numeric(10, 7))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    farming_period: Mapped["FarmingPeriod"] = relationship(  # noqa: F821
        back_populates="reports"
    )
    media: Mapped[list["VisitMedia"]] = relationship(back_populates="report")
    drug_applications: Mapped[list["AgriDrugApplication"]] = relationship(
        back_populates="report"
    )


class VisitMedia(Base):
    __tablename__ = "visit_media"

    visit_media_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reports.report_id"), nullable=False
    )
    media_type: Mapped[str] = mapped_column(Text, nullable=False)
    file_url: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    report: Mapped["Report"] = relationship(back_populates="media")


class AgriDrugApplication(Base):
    __tablename__ = "agri_drug_applications"

    drug_application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reports.report_id"), nullable=False
    )
    agri_drug_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agri_drugs.agri_drug_id"), nullable=False
    )
    dosage_quantity: Mapped[float | None] = mapped_column(Numeric(15, 2))
    dosage_unit: Mapped[str | None] = mapped_column(Text)
    application_date: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    report: Mapped["Report"] = relationship(back_populates="drug_applications")
