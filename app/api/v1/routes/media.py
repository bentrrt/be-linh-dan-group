"""Visit media and drug-application attachment endpoints (FR-08)."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import instances as crud
from app.models import VisitMedia
from app.schemas.report import (
    AgriDrugApplicationCreate,
    AgriDrugApplicationRead,
    VisitMediaCreate,
    VisitMediaRead,
)

router = APIRouter(prefix="/reports", tags=["reports: attachments"])


@router.post(
    "/media",
    response_model=VisitMediaRead,
    status_code=status.HTTP_201_CREATED,
)
def add_media(payload: VisitMediaCreate, db: Session = Depends(get_db)):
    """Attach a photo or video to an existing report."""
    if crud.report.get(db, payload.report_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Report not found")
    return crud.visit_media.create(db, payload.model_dump())


@router.get("/{report_id}/media", response_model=list[VisitMediaRead])
def list_report_media(report_id: uuid.UUID, db: Session = Depends(get_db)):
    if crud.report.get(db, report_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Report not found")
    stmt = (
        select(VisitMedia)
        .where(VisitMedia.report_id == report_id, VisitMedia.is_active.is_(True))
        .order_by(VisitMedia.created_at.desc())
    )
    return list(db.execute(stmt).scalars().all())


@router.post(
    "/drug-applications",
    response_model=AgriDrugApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def add_drug_application(
    payload: AgriDrugApplicationCreate, db: Session = Depends(get_db)
):
    """Record an agricultural-drug application against a report."""
    if crud.report.get(db, payload.report_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Report not found")
    if crud.agri_drug.get(db, payload.agri_drug_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Agri drug not found")
    return crud.agri_drug_application.create(db, payload.model_dump())
