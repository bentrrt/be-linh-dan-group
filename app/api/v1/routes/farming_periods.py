"""Farming period (growing season) endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import instances as crud
from app.schemas.farming import (
    FarmingPeriodCreate,
    FarmingPeriodRead,
    FarmingPeriodUpdate,
)

router = APIRouter(prefix="/farming-periods", tags=["farming-periods"])


@router.get("", response_model=list[FarmingPeriodRead])
def list_farming_periods(
    skip: int = 0,
    limit: int = 100,
    farmer_id: uuid.UUID | None = Query(default=None),
    db: Session = Depends(get_db),
):
    if farmer_id is not None:
        stmt = (
            select(crud.farming_period.model)
            .where(
                crud.farming_period.model.is_active.is_(True),
                crud.farming_period.model.farmer_id == farmer_id,
            )
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())
    return crud.farming_period.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=FarmingPeriodRead, status_code=status.HTTP_201_CREATED)
def create_farming_period(payload: FarmingPeriodCreate, db: Session = Depends(get_db)):
    if crud.farmer.get(db, payload.farmer_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Farmer not found")
    if crud.crop_type.get(db, payload.crop_type_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Crop type not found")
    return crud.farming_period.create(db, payload.model_dump())


@router.get("/{farming_period_id}", response_model=FarmingPeriodRead)
def get_farming_period(farming_period_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.farming_period.get(db, farming_period_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Farming period not found")
    return obj


@router.patch("/{farming_period_id}", response_model=FarmingPeriodRead)
def update_farming_period(
    farming_period_id: uuid.UUID,
    payload: FarmingPeriodUpdate,
    db: Session = Depends(get_db),
):
    obj = crud.farming_period.get(db, farming_period_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Farming period not found")
    return crud.farming_period.update(db, obj, payload.model_dump(exclude_unset=True))


@router.delete("/{farming_period_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farming_period(farming_period_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.farming_period.get(db, farming_period_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Farming period not found")
    crud.farming_period.soft_delete(db, obj)
