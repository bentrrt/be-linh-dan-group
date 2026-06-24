"""Yield (harvest) report endpoints (FR-03)."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.v1.routes._report_helpers import create_report, validate_report_refs
from app.core.database import get_db
from app.models import ReportType
from app.schemas.report import ReportRead, YieldReportCreate

router = APIRouter(prefix="/reports/yield", tags=["reports: yield"])


@router.post("", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
def create_yield_report(payload: YieldReportCreate, db: Session = Depends(get_db)):
    """FR-03: record a daily harvest yield for a farming period."""
    validate_report_refs(db, payload.farming_period_id, payload.created_by)
    content = payload.content.model_dump(mode="json")
    return create_report(
        db,
        report_type=ReportType.YIELD,
        farming_period_id=payload.farming_period_id,
        created_by=payload.created_by,
        content=content,
        submitted_mac_address=payload.submitted_mac_address,
        gps_lat=payload.gps_lat,
        gps_long=payload.gps_long,
    )
