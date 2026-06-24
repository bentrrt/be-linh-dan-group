"""Shared helpers for report-creation endpoints."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import instances as crud
from app.models import Report, ReportType


def validate_report_refs(db: Session, farming_period_id, created_by) -> None:
    """Ensure the farming period and author user exist before inserting a report."""
    if crud.farming_period.get(db, farming_period_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Farming period not found")
    if crud.user.get(db, created_by) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Author user not found")


def create_report(
    db: Session,
    *,
    report_type: ReportType,
    farming_period_id,
    created_by,
    content: dict,
    submitted_mac_address: str | None,
    gps_lat: float | None,
    gps_long: float | None,
) -> Report:
    """Insert a report row of the given type."""
    return crud.report.create(
        db,
        {
            "report_type": report_type,
            "farming_period_id": farming_period_id,
            "created_by": created_by,
            "content": content,
            "submitted_mac_address": submitted_mac_address,
            "gps_lat": gps_lat,
            "gps_long": gps_long,
        },
    )
