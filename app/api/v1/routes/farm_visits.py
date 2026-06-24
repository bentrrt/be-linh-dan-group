"""Farm-visit report endpoints (FR-08) including media and drug applications."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.v1.routes._report_helpers import create_report, validate_report_refs
from app.core.database import get_db
from app.models import ReportType
from app.schemas.report import FarmVisitReportCreate, ReportRead

router = APIRouter(prefix="/reports/farm-visit", tags=["reports: farm-visit"])


@router.post("", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
def create_farm_visit_report(
    payload: FarmVisitReportCreate, db: Session = Depends(get_db)
):
    """FR-08: record an on-site farm visit (status + notes).

    Photos/videos and drug applications are attached afterwards via the
    /reports/media and /reports/{id}/drug-applications endpoints, since they
    reference the created report.
    """
    validate_report_refs(db, payload.farming_period_id, payload.created_by)
    content = payload.content.model_dump(mode="json")
    return create_report(
        db,
        report_type=ReportType.FARM_VISIT,
        farming_period_id=payload.farming_period_id,
        created_by=payload.created_by,
        content=content,
        submitted_mac_address=payload.submitted_mac_address,
        gps_lat=payload.gps_lat,
        gps_long=payload.gps_long,
    )
