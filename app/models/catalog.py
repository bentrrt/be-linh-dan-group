"""Catalog models: crop types and agricultural drugs."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CropType(Base):
    __tablename__ = "crop_types"

    crop_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    crop_code: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    crop_name: Mapped[str] = mapped_column(Text, nullable=False)
    default_unit: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class AgriDrug(Base):
    __tablename__ = "agri_drugs"

    agri_drug_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    drug_name: Mapped[str] = mapped_column(Text, nullable=False)
    drug_details: Mapped[dict | None] = mapped_column(JSONB)
    default_unit: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
