"""Schemas for reports, media, and drug applications.

A single `reports` table stores three report kinds distinguished by
`report_type`, each with a different JSON `content` shape that mirrors the
keys enforced by the `validate_report_content` database trigger.
"""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.report import ReportType
from app.schemas.common import ORMModel


# ── Report content payloads (must match the DB trigger's required keys) ───────
class YieldContent(BaseModel):
    """Content for a YIELD report (FR-03)."""

    harvest_date: date
    quantity_kg: float
    quantity_bundle: float
    residue_status: bool = Field(description="True if residue is still present")
    expected_residue_clear_date: date | None = None


class FarmingStageContent(BaseModel):
    """Content for a FARMING_STAGE (resting) report (FR-05)."""

    stage_type: str
    start_date: date
    # Optional on input: the system defaults it to start_date + 1 month.
    expected_resume_date: date | None = None


class FarmVisitContent(BaseModel):
    """Content for a FARM_VISIT report (FR-08)."""

    general_status: str
    notes: str


# ── Common report fields ─────────────────────────────────────────────────────
class _ReportBase(BaseModel):
    farming_period_id: uuid.UUID
    created_by: uuid.UUID
    submitted_mac_address: str | None = None
    gps_lat: float | None = Field(default=None, ge=-90, le=90)
    gps_long: float | None = Field(default=None, ge=-180, le=180)


# ── Per-type create schemas ──────────────────────────────────────────────────
class YieldReportCreate(_ReportBase):
    content: YieldContent


class FarmingStageReportCreate(_ReportBase):
    content: FarmingStageContent


class FarmVisitReportCreate(_ReportBase):
    content: FarmVisitContent


# ── Read schema ──────────────────────────────────────────────────────────────
class ReportRead(ORMModel):
    report_id: uuid.UUID
    farming_period_id: uuid.UUID
    created_by: uuid.UUID
    report_type: ReportType
    content: dict
    submitted_mac_address: str | None
    gps_lat: float | None
    gps_long: float | None
    is_active: bool
    created_at: datetime


# ── Visit media ──────────────────────────────────────────────────────────────
class VisitMediaCreate(BaseModel):
    report_id: uuid.UUID
    media_type: str
    file_url: str


class VisitMediaRead(ORMModel):
    visit_media_id: uuid.UUID
    report_id: uuid.UUID
    media_type: str
    file_url: str
    is_active: bool
    created_at: datetime


# ── Drug applications ────────────────────────────────────────────────────────
class AgriDrugApplicationCreate(BaseModel):
    report_id: uuid.UUID
    agri_drug_id: uuid.UUID
    dosage_quantity: float | None = None
    dosage_unit: str | None = None
    application_date: date | None = None
    notes: str | None = None


class AgriDrugApplicationRead(ORMModel):
    drug_application_id: uuid.UUID
    report_id: uuid.UUID
    agri_drug_id: uuid.UUID
    dosage_quantity: float | None
    dosage_unit: str | None
    application_date: date | None
    notes: str | None
    is_active: bool
    created_at: datetime
