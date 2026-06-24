"""Role endpoints (FR-01)."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import instances as crud
from app.schemas.user import RoleCreate, RoleRead

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=list[RoleRead])
def list_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.role.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role(payload: RoleCreate, db: Session = Depends(get_db)):
    return crud.role.create(db, payload.model_dump())


@router.get("/{role_id}", response_model=RoleRead)
def get_role(role_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.role.get(db, role_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")
    return obj


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.role.get(db, role_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")
    crud.role.soft_delete(db, obj)
