"""Farmer endpoints (FR-02 create, FR-07 detail lookup)."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import instances as crud
from app.models import FarmingPeriod, Report, VisitMedia
from app.schemas.farmer import FarmerCreate, FarmerRead, FarmerUpdate
from app.schemas.report import VisitMediaRead

router = APIRouter(prefix="/farmers", tags=["farmers"])


@router.get("", response_model=list[FarmerRead])
def list_farmers(
    skip: int = 0,
    limit: int = 100,
    name: str | None = Query(default=None, description="Case-insensitive name filter"),
    db: Session = Depends(get_db),
):
    if name:
        stmt = (
            select(crud.farmer.model)
            .where(
                crud.farmer.model.is_active.is_(True),
                crud.farmer.model.farmer_name.ilike(f"%{name}%"),
            )
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())
    return crud.farmer.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=FarmerRead, status_code=status.HTTP_201_CREATED)
def create_farmer(payload: FarmerCreate, db: Session = Depends(get_db)):
    return crud.farmer.create(db, payload.model_dump())


@router.get("/{farmer_id}", response_model=FarmerRead)
def get_farmer(farmer_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.farmer.get(db, farmer_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Farmer not found")
    return obj


@router.get("/{farmer_id}/media", response_model=list[VisitMediaRead])
def get_farmer_media(
    farmer_id: uuid.UUID,
    limit: int = Query(default=5, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """FR-07: the most recent media captured at this farmer's site."""
    if crud.farmer.get(db, farmer_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Farmer not found")
    stmt = (
        select(VisitMedia)
        .join(Report, VisitMedia.report_id == Report.report_id)
        .join(
            FarmingPeriod,
            Report.farming_period_id == FarmingPeriod.farming_period_id,
        )
        .where(
            FarmingPeriod.farmer_id == farmer_id,
            VisitMedia.is_active.is_(True),
        )
        .order_by(VisitMedia.created_at.desc())
        .limit(limit)
    )
    return list(db.execute(stmt).scalars().all())


@router.patch("/{farmer_id}", response_model=FarmerRead)
def update_farmer(
    farmer_id: uuid.UUID, payload: FarmerUpdate, db: Session = Depends(get_db)
):
    obj = crud.farmer.get(db, farmer_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Farmer not found")
    return crud.farmer.update(db, obj, payload.model_dump(exclude_unset=True))


@router.delete("/{farmer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farmer(farmer_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.farmer.get(db, farmer_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Farmer not found")
    crud.farmer.soft_delete(db, obj)
