"""Crop type catalog endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import instances as crud
from app.schemas.catalog import CropTypeCreate, CropTypeRead

router = APIRouter(prefix="/crop-types", tags=["crop-types"])


@router.get("", response_model=list[CropTypeRead])
def list_crop_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.crop_type.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=CropTypeRead, status_code=status.HTTP_201_CREATED)
def create_crop_type(payload: CropTypeCreate, db: Session = Depends(get_db)):
    return crud.crop_type.create(db, payload.model_dump())


@router.get("/{crop_type_id}", response_model=CropTypeRead)
def get_crop_type(crop_type_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.crop_type.get(db, crop_type_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Crop type not found")
    return obj


@router.delete("/{crop_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_crop_type(crop_type_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.crop_type.get(db, crop_type_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Crop type not found")
    crud.crop_type.soft_delete(db, obj)
