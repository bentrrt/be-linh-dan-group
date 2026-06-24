"""Schemas for users, roles, and user-role assignment (FR-01)."""

import uuid
from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


# ── Roles ────────────────────────────────────────────────────────────────────
class RoleCreate(BaseModel):
    role_code: str
    role_name: str


class RoleRead(ORMModel):
    role_id: uuid.UUID
    role_code: str
    role_name: str
    is_active: bool
    created_at: datetime


# ── Users ────────────────────────────────────────────────────────────────────
class UserCreate(BaseModel):
    full_name: str | None = None
    zalo_id: str | None = None
    registered_mac_address: str | None = None
    registered_device_fingerprint: str | None = None
    status: str | None = None


class UserUpdate(BaseModel):
    full_name: str | None = None
    zalo_id: str | None = None
    registered_mac_address: str | None = None
    registered_device_fingerprint: str | None = None
    status: str | None = None


class UserRead(ORMModel):
    user_id: uuid.UUID
    full_name: str | None
    zalo_id: str | None
    registered_mac_address: str | None
    registered_device_fingerprint: str | None
    status: str | None
    is_active: bool
    created_at: datetime


# ── User-role link ───────────────────────────────────────────────────────────
class UserRoleCreate(BaseModel):
    user_id: uuid.UUID
    role_id: uuid.UUID


class UserRoleRead(ORMModel):
    user_role_id: uuid.UUID
    user_id: uuid.UUID
    role_id: uuid.UUID
    is_active: bool
    created_at: datetime
