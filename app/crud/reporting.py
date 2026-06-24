"""Aggregation queries backing the reporting endpoints (FR-04, FR-06, FR-11)."""

import uuid
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Farmer, FarmingPeriod, Report, ReportType, VisitMedia
from app.schemas.reporting import (
    FarmVisitQueryResult,
    FarmVisitRow,
    HarvestRestReport,
    HarvestRestRow,
    YieldDailyReport,
    YieldReportRow,
)


def _content_text(column, key: str):
    """Return a JSONB key as text for filtering/sorting."""
    return column[key].astext


def get_yield_daily_report(db: Session, report_date: date) -> YieldDailyReport:
    """FR-04: yield for a harvest date, split by residue status."""
    target = report_date.isoformat()
    stmt = (
        select(Report, Farmer.farmer_id, Farmer.farmer_name)
        .join(FarmingPeriod, Report.farming_period_id == FarmingPeriod.farming_period_id)
        .join(Farmer, FarmingPeriod.farmer_id == Farmer.farmer_id)
        .where(
            Report.report_type == ReportType.YIELD,
            Report.is_active.is_(True),
            _content_text(Report.content, "harvest_date") == target,
        )
        .order_by(_content_text(Report.content, "harvest_date").desc())
    )

    with_residue: list[YieldReportRow] = []
    without_residue: list[YieldReportRow] = []
    total_with = 0.0
    total_without = 0.0

    for report, farmer_id, farmer_name in db.execute(stmt).all():
        content = report.content or {}
        qty_kg = content.get("quantity_kg")
        row = YieldReportRow(
            report_id=report.report_id,
            farmer_id=farmer_id,
            farmer_name=farmer_name,
            harvest_date=content.get("harvest_date"),
            quantity_kg=qty_kg,
            quantity_bundle=content.get("quantity_bundle"),
            residue_status=content.get("residue_status"),
            expected_residue_clear_date=content.get("expected_residue_clear_date"),
        )
        if content.get("residue_status"):
            with_residue.append(row)
            total_with += float(qty_kg or 0)
        else:
            without_residue.append(row)
            total_without += float(qty_kg or 0)

    return YieldDailyReport(
        report_date=report_date,
        with_residue=with_residue,
        without_residue=without_residue,
        total_with_residue_kg=total_with,
        total_without_residue_kg=total_without,
    )


def get_harvest_rest_report(
    db: Session, date_from: date, date_to: date
) -> HarvestRestReport:
    """FR-06: harvest (YIELD) and resting (FARMING_STAGE) records in a window."""
    stmt = (
        select(Report, Farmer.farmer_id, Farmer.farmer_name)
        .join(FarmingPeriod, Report.farming_period_id == FarmingPeriod.farming_period_id)
        .join(Farmer, FarmingPeriod.farmer_id == Farmer.farmer_id)
        .where(
            Report.report_type.in_([ReportType.YIELD, ReportType.FARMING_STAGE]),
            Report.is_active.is_(True),
            Report.created_at >= date_from,
            Report.created_at < date_to,
        )
        .order_by(Report.created_at.asc())
    )

    harvest: list[HarvestRestRow] = []
    resting: list[HarvestRestRow] = []
    for report, farmer_id, farmer_name in db.execute(stmt).all():
        row = HarvestRestRow(
            report_id=report.report_id,
            farmer_id=farmer_id,
            farmer_name=farmer_name,
            report_type=report.report_type.value,
            created_at=report.created_at,
            content=report.content or {},
        )
        if report.report_type == ReportType.YIELD:
            harvest.append(row)
        else:
            resting.append(row)

    return HarvestRestReport(
        date_from=date_from,
        date_to=date_to,
        harvest=harvest,
        resting=resting,
    )


def query_farm_visits(
    db: Session,
    *,
    farmer_id: uuid.UUID | None = None,
    visit_date: date | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
) -> FarmVisitQueryResult:
    """FR-11: farm-visit reports filtered by farmer and/or date range."""
    stmt = (
        select(Report, Farmer.farmer_id, Farmer.farmer_name)
        .join(FarmingPeriod, Report.farming_period_id == FarmingPeriod.farming_period_id)
        .join(Farmer, FarmingPeriod.farmer_id == Farmer.farmer_id)
        .where(
            Report.report_type == ReportType.FARM_VISIT,
            Report.is_active.is_(True),
        )
        .order_by(Report.created_at.desc())
    )
    if farmer_id is not None:
        stmt = stmt.where(Farmer.farmer_id == farmer_id)
    if visit_date is not None:
        next_day = visit_date + timedelta(days=1)
        stmt = stmt.where(
            Report.created_at >= visit_date, Report.created_at < next_day
        )
    if date_from is not None:
        stmt = stmt.where(Report.created_at >= date_from)
    if date_to is not None:
        stmt = stmt.where(Report.created_at < date_to)

    visits: list[FarmVisitRow] = []
    for report, fid, fname in db.execute(stmt).all():
        media_stmt = (
            select(VisitMedia)
            .where(VisitMedia.report_id == report.report_id, VisitMedia.is_active.is_(True))
            .order_by(VisitMedia.created_at.desc())
        )
        media = list(db.execute(media_stmt).scalars().all())
        content = report.content or {}
        visits.append(
            FarmVisitRow(
                report_id=report.report_id,
                farmer_id=fid,
                farmer_name=fname,
                created_at=report.created_at,
                general_status=content.get("general_status"),
                notes=content.get("notes"),
                media=media,
            )
        )

    return FarmVisitQueryResult(visits=visits)
