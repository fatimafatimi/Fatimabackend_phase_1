from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from handler.role_handler import create_role, assign_permissions_to_role, get_role_with_permissions
from dependencies.permissions import require_permission
from pydantic import BaseModel
from typing import List

role_router = APIRouter(prefix="/roles", tags=["Roles"])


class PermissionAssign(BaseModel):
    permission_names: List[str]


@role_router.post("/")
def create_role_route(
    name: str,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("manage_roles"))
):
    return create_role(db, name)


@role_router.post("/{role_id}/permissions")
def assign_permissions_route(
    role_id: int,
    permissions: PermissionAssign,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("manage_roles"))
):
    return assign_permissions_to_role(db, role_id, permissions.permission_names)


@role_router.get("/{role_id}")
def get_role_route(
    role_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("manage_roles"))
):
    return get_role_with_permissions(db, role_id)
