"""Aggregated reporting endpoints (FR-04, FR-06, FR-11)."""

import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import reporting as reporting_crud
from app.schemas.reporting import (
    FarmVisitQueryResult,
    HarvestRestReport,
    YieldDailyReport,
)

router = APIRouter(prefix="/reporting", tags=["reporting"])


@router.get("/yield", response_model=YieldDailyReport)
def yield_daily_report(
    report_date: date = Query(..., description="Harvest date to report on"),
    db: Session = Depends(get_db),
):
    """FR-04: daily yield split into residue / no-residue groups with totals."""
    return reporting_crud.get_yield_daily_report(db, report_date)


@router.get("/harvest-rest", response_model=HarvestRestReport)
def harvest_rest_report(
    date_from: date = Query(..., description="Start of the window (inclusive)"),
    date_to: date = Query(..., description="End of the window (exclusive)"),
    db: Session = Depends(get_db),
):
    """FR-06: harvest and resting records within a date window."""
    return reporting_crud.get_harvest_rest_report(db, date_from, date_to)


@router.get("/farm-visits", response_model=FarmVisitQueryResult)
def farm_visit_query(
    farmer_id: uuid.UUID | None = Query(default=None),
    visit_date: date | None = Query(default=None, description="Exact visit day"),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    db: Session = Depends(get_db),
):
    """FR-11: query farm-visit reports by farmer and/or date range."""
    return reporting_crud.query_farm_visits(
        db,
        farmer_id=farmer_id,
        visit_date=visit_date,
        date_from=date_from,
        date_to=date_to,
    )
