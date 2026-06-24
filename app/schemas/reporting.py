"""Response schemas for aggregated reports (FR-04, FR-06, FR-11)."""

import uuid
from datetime import date, datetime

from pydantic import BaseModel

from app.schemas.report import VisitMediaRead


# ── FR-04: daily yield report (residue / no-residue split) ───────────────────
class YieldReportRow(BaseModel):
    report_id: uuid.UUID
    farmer_id: uuid.UUID
    farmer_name: str
    harvest_date: date | None
    quantity_kg: float | None
    quantity_bundle: float | None
    residue_status: bool | None
    expected_residue_clear_date: date | None


class YieldDailyReport(BaseModel):
    report_date: date
    with_residue: list[YieldReportRow]
    without_residue: list[YieldReportRow]
    total_with_residue_kg: float
    total_without_residue_kg: float


# ── FR-06: harvest & rest timeline ───────────────────────────────────────────
class HarvestRestRow(BaseModel):
    report_id: uuid.UUID
    farmer_id: uuid.UUID
    farmer_name: str
    report_type: str
    created_at: datetime
    content: dict


class HarvestRestReport(BaseModel):
    date_from: date
    date_to: date
    harvest: list[HarvestRestRow]
    resting: list[HarvestRestRow]


# ── FR-11: farm-visit query ──────────────────────────────────────────────────
class FarmVisitRow(BaseModel):
    report_id: uuid.UUID
    farmer_id: uuid.UUID
    farmer_name: str
    created_at: datetime
    general_status: str | None
    notes: str | None
    media: list[VisitMediaRead]


class FarmVisitQueryResult(BaseModel):
    visits: list[FarmVisitRow]
