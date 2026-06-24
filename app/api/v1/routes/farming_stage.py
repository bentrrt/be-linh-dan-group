"""Farming-stage (resting) report endpoints (FR-05)."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.v1.routes._report_helpers import create_report, validate_report_refs
from app.core.database import get_db
from app.models import ReportType
from app.schemas.report import FarmingStageReportCreate, ReportRead
from app.utils.dates import add_one_month

router = APIRouter(prefix="/reports/farming-stage", tags=["reports: farming-stage"])


@router.post("", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
def create_farming_stage_report(
    payload: FarmingStageReportCreate, db: Session = Depends(get_db)
):
    """FR-05: record a resting period; resume date defaults to start + 1 month."""
    validate_report_refs(db, payload.farming_period_id, payload.created_by)
    content = payload.content.model_dump(mode="json")
    if content.get("expected_resume_date") is None:
        content["expected_resume_date"] = add_one_month(
            payload.content.start_date
        ).isoformat()
    return create_report(
        db,
        report_type=ReportType.FARMING_STAGE,
        farming_period_id=payload.farming_period_id,
        created_by=payload.created_by,
        content=content,
        submitted_mac_address=payload.submitted_mac_address,
        gps_lat=payload.gps_lat,
        gps_long=payload.gps_long,
    )
