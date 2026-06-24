"""User and user-role assignment endpoints (FR-01)."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import instances as crud
from app.schemas.user import (
    UserCreate,
    UserRead,
    UserRoleCreate,
    UserRoleRead,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.user.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return crud.user.create(db, payload.model_dump())


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.user.get(db, user_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return obj


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: uuid.UUID, payload: UserUpdate, db: Session = Depends(get_db)):
    obj = crud.user.get(db, user_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return crud.user.update(db, obj, payload.model_dump(exclude_unset=True))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.user.get(db, user_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    crud.user.soft_delete(db, obj)


# ── Role assignment ──────────────────────────────────────────────────────────
@router.post(
    "/roles/assign",
    response_model=UserRoleRead,
    status_code=status.HTTP_201_CREATED,
    tags=["user-roles"],
)
def assign_role(payload: UserRoleCreate, db: Session = Depends(get_db)):
    if crud.user.get(db, payload.user_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    if crud.role.get(db, payload.role_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")
    return crud.user_role.create(db, payload.model_dump())


@router.delete(
    "/roles/{user_role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["user-roles"],
)
def revoke_role(user_role_id: uuid.UUID, db: Session = Depends(get_db)):
    obj = crud.user_role.get(db, user_role_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Assignment not found")
    crud.user_role.soft_delete(db, obj)
