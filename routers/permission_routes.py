from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from handler.permission_handler import create_permission, list_permissions
from schemas.permission import PermissionCreate, PermissionResponse
from dependencies.permissions import require_permission
from typing import List

permission_router = APIRouter(prefix="/permissions", tags=["Permissions"])


@permission_router.post("/", response_model=PermissionResponse)
def create_permission_route(
    perm_data: PermissionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("manage_permissions"))
):
    return create_permission(db, perm_data)


@permission_router.get("/", response_model=List[PermissionResponse])
def list_permissions_route(
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("manage_permissions"))
):
    return list_permissions(db)
