# routers/role_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from handler.role_handler import (
    create_role,
    assign_permissions_to_role,
    get_role_with_permissions,
    list_roles,           
)
from dependencies.permissions import require_permission
from pydantic import BaseModel
from typing import List
from schemas.role import RoleCreate, RoleResponse
from models.user import User

role_router = APIRouter(prefix="/roles", tags=["Roles"])


class PermissionAssign(BaseModel):
    permission_names: List[str]


@role_router.post("/", response_model=RoleResponse)
def create_role_route(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_roles"))
):
    return create_role(db, role_data, current_user)


@role_router.get("/", response_model=List[RoleResponse])
def list_roles_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("view_roles"))
):
    return list_roles(db, current_user)


@role_router.post("/{role_id}/permissions", response_model=RoleResponse)
def assign_permissions_route(
    role_id: int,
    permissions: PermissionAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_roles"))
):
    return assign_permissions_to_role(db, role_id, permissions.permission_names, current_user)


@role_router.get("/{role_id}")
def get_role_route(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_roles"))
):
    return get_role_with_permissions(db, role_id, current_user)