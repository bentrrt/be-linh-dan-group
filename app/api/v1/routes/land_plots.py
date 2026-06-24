"""Land plot endpoints (supports FR-02 location/area tracking)."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import instances as crud
from app.schemas.farmer import (
    FarmerLandPlotCreate,
    FarmerLandPlotRead,
    LandPlotCreate,
    LandPlotRead,
)

router = APIRouter(prefix="/land-plots", tags=["land-plots"])


@router.get("", response_model=list[LandPlotRead])
def list_land_plots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.land_plot.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=LandPlotRead, status_code=status.HTTP_201_CREATED)
def create_land_plot(payload: LandPlotCreate, db: Session = Depends(get_db)):
    return crud.land_plot.create(db, payload.model_dump())


@router.get("/{land_plot_id}", response_model=LandPlotRead)
def get_land_plot(land_plot_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.land_plot.get(db, land_plot_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Land plot not found")
    return obj


@router.delete("/{land_plot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_land_plot(land_plot_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.land_plot.get(db, land_plot_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Land plot not found")
    crud.land_plot.soft_delete(db, obj)


# ── Farmer ↔ land-plot link ──────────────────────────────────────────────────
@router.post(
    "/links",
    response_model=FarmerLandPlotRead,
    status_code=status.HTTP_201_CREATED,
)
def link_farmer_land_plot(payload: FarmerLandPlotCreate, db: Session = Depends(get_db)):
    if crud.farmer.get(db, payload.farmer_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Farmer not found")
    if crud.land_plot.get(db, payload.land_plot_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Land plot not found")
    return crud.farmer_land_plot.create(db, payload.model_dump())
