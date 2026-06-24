"""Schemas for farmers, land plots, and their link (FR-02, FR-07, FR-09)."""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


# ── Land plots ───────────────────────────────────────────────────────────────
class LandPlotCreate(BaseModel):
    land_plot_name: str
    address_text: str | None = None
    total_area_m2: float | None = None
    boundary_geojson: dict | None = None
    public_code: str | None = None


class LandPlotRead(ORMModel):
    land_plot_id: uuid.UUID
    land_plot_name: str
    address_text: str | None
    total_area_m2: float | None
    boundary_geojson: dict | None
    public_code: str | None
    is_active: bool
    created_at: datetime


# ── Farmers ──────────────────────────────────────────────────────────────────
class FarmerCreate(BaseModel):
    farmer_name: str
    phone_number: str | None = None
    public_code: str | None = Field(
        default=None, description="URL to the farmer's QR code image"
    )
    avatar_url: str | None = None


class FarmerUpdate(BaseModel):
    farmer_name: str | None = None
    phone_number: str | None = None
    public_code: str | None = None
    avatar_url: str | None = None


class FarmerRead(ORMModel):
    farmer_id: uuid.UUID
    farmer_name: str
    phone_number: str | None
    public_code: str | None
    avatar_url: str | None
    is_active: bool
    created_at: datetime


class FarmerQRRead(ORMModel):
    """Minimal farmer payload for QR export (FR-09)."""

    farmer_id: uuid.UUID
    farmer_name: str
    phone_number: str | None
    public_code: str | None
    created_at: datetime


# ── Farmer-land-plot link ────────────────────────────────────────────────────
class FarmerLandPlotCreate(BaseModel):
    farmer_id: uuid.UUID
    land_plot_id: uuid.UUID


class FarmerLandPlotRead(ORMModel):
    farmer_land_plot_id: uuid.UUID
    farmer_id: uuid.UUID
    land_plot_id: uuid.UUID
    inactive_date: date | None
    created_at: datetime
