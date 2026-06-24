"""Farmer QR-code export endpoint (FR-09).

Returns the data needed to build the printable QR list (farmer name, phone,
and the QR image URL stored in `public_code`). PDF rendering itself is handled
by a later phase / the Zalo Bot service.
"""

from datetime import date, datetime, time

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Farmer
from app.schemas.farmer import FarmerQRRead

router = APIRouter(prefix="/farmers/qr", tags=["farmers: qr"])


@router.get("", response_model=list[FarmerQRRead])
def export_farmer_qr(
    name: str | None = Query(default=None, description="Filter by farmer name"),
    created_from: date | None = Query(
        default=None, description="Only farmers added on/after this date"
    ),
    created_to: date | None = Query(
        default=None, description="Only farmers added on/before this date"
    ),
    db: Session = Depends(get_db),
):
    """FR-09: list farmers (optionally filtered) with their QR image URLs."""
    stmt = select(Farmer).where(Farmer.is_active.is_(True))
    if name:
        stmt = stmt.where(Farmer.farmer_name.ilike(f"%{name}%"))
    if created_from:
        stmt = stmt.where(Farmer.created_at >= datetime.combine(created_from, time.min))
    if created_to:
        stmt = stmt.where(Farmer.created_at <= datetime.combine(created_to, time.max))
    stmt = stmt.order_by(Farmer.created_at.desc())
    return list(db.execute(stmt).scalars().all())
