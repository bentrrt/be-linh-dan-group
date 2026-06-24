"""Generic CRUD base with soft-delete awareness.

All tables in this schema use an `is_active` boolean for soft deletes, so the
default read operations filter on `is_active = TRUE`.
"""

from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    """Reusable create/read/update/soft-delete operations for one model."""

    def __init__(self, model: type[ModelType], pk_name: str) -> None:
        self.model = model
        self.pk_name = pk_name

    @property
    def _pk_column(self) -> Any:
        return getattr(self.model, self.pk_name)

    def get(self, db: Session, obj_id: Any, *, active_only: bool = True) -> ModelType | None:
        stmt = select(self.model).where(self._pk_column == obj_id)
        if active_only and hasattr(self.model, "is_active"):
            stmt = stmt.where(self.model.is_active.is_(True))
        return db.execute(stmt).scalar_one_or_none()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True,
    ) -> list[ModelType]:
        stmt = select(self.model)
        if active_only and hasattr(self.model, "is_active"):
            stmt = stmt.where(self.model.is_active.is_(True))
        stmt = stmt.offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())

    def create(self, db: Session, data: dict[str, Any]) -> ModelType:
        obj = self.model(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: ModelType, data: dict[str, Any]) -> ModelType:
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def soft_delete(self, db: Session, db_obj: ModelType) -> ModelType:
        if hasattr(db_obj, "is_active"):
            db_obj.is_active = False  # type: ignore[attr-defined]
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj
