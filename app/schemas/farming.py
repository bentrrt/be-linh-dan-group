"""Schemas for farming periods (growing seasons)."""

import uuid
from datetime import date, datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


class FarmingPeriodCreate(BaseModel):
    farmer_id: uuid.UUID
    crop_type_id: uuid.UUID
    cultivated_area_m2: float | None = None
    cultivated_boundary_geojson: dict | None = None
    start_date: date
    end_date: date | None = None
    status: str | None = None
    public_code: str | None = None


class FarmingPeriodUpdate(BaseModel):
    crop_type_id: uuid.UUID | None = None
    cultivated_area_m2: float | None = None
    cultivated_boundary_geojson: dict | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = None
    public_code: str | None = None


class FarmingPeriodRead(ORMModel):
    farming_period_id: uuid.UUID
    farmer_id: uuid.UUID
    crop_type_id: uuid.UUID
    cultivated_area_m2: float | None
    cultivated_boundary_geojson: dict | None
    start_date: date
    end_date: date | None
    status: str | None
    public_code: str | None
    is_active: bool
    created_at: datetime
