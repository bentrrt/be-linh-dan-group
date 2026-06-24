"""Agricultural drug catalog endpoints (used by FR-08 drug applications)."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import instances as crud
from app.schemas.catalog import AgriDrugCreate, AgriDrugRead

router = APIRouter(prefix="/agri-drugs", tags=["agri-drugs"])


@router.get("", response_model=list[AgriDrugRead])
def list_agri_drugs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.agri_drug.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=AgriDrugRead, status_code=status.HTTP_201_CREATED)
def create_agri_drug(payload: AgriDrugCreate, db: Session = Depends(get_db)):
    return crud.agri_drug.create(db, payload.model_dump())


@router.get("/{agri_drug_id}", response_model=AgriDrugRead)
def get_agri_drug(agri_drug_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.agri_drug.get(db, agri_drug_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Agri drug not found")
    return obj


@router.delete("/{agri_drug_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agri_drug(agri_drug_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.agri_drug.get(db, agri_drug_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Agri drug not found")
    crud.agri_drug.soft_delete(db, obj)
