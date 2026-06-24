"""Schemas for catalog entities: crop types and agricultural drugs."""

import uuid
from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


# ── Crop types ───────────────────────────────────────────────────────────────
class CropTypeCreate(BaseModel):
    crop_code: str
    crop_name: str
    default_unit: str | None = None


class CropTypeRead(ORMModel):
    crop_type_id: uuid.UUID
    crop_code: str
    crop_name: str
    default_unit: str | None
    is_active: bool
    created_at: datetime


# ── Agricultural drugs ───────────────────────────────────────────────────────
class AgriDrugCreate(BaseModel):
    drug_name: str
    drug_details: dict | None = None
    default_unit: str | None = None


class AgriDrugRead(ORMModel):
    agri_drug_id: uuid.UUID
    drug_name: str
    drug_details: dict | None
    default_unit: str | None
    is_active: bool
    created_at: datetime
