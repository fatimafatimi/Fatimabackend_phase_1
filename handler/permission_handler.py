# handler/permission_handler.py
from models.permission import Permission
from schemas.permission import PermissionCreate, PermissionResponse
from sqlalchemy.orm import Session
from typing import List
from models.user import User
from fastapi import HTTPException

def create_permission(db: Session, perm_data: PermissionCreate, current_user: User) -> PermissionResponse:
    # Only tenant admins or super admins can create permissions
    if not current_user.is_super_admin and current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Only tenant admins can create permissions")

    existing_perm = db.query(Permission).filter(
        Permission.name == perm_data.name
    )
    if not current_user.is_super_admin:
        existing_perm = existing_perm.filter(Permission.tenant_id == current_user.tenant_id)
    existing_perm = existing_perm.first()

    if existing_perm:
        return PermissionResponse.from_orm(existing_perm)

    permission = Permission(name=perm_data.name, tenant_id=current_user.tenant_id)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return PermissionResponse.from_orm(permission)


def list_permissions(db: Session, current_user: User) -> List[PermissionResponse]:
    query = db.query(Permission)
    if not current_user.is_super_admin:
        query = query.filter(Permission.tenant_id == current_user.tenant_id)
    permissions = query.all()
    return [PermissionResponse.from_orm(p) for p in permissions]