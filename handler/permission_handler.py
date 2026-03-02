from models.permission import Permission
from schemas.permission import PermissionCreate, PermissionResponse
from sqlalchemy.orm import Session
from typing import List

def create_permission(db: Session, perm_data: PermissionCreate) -> PermissionResponse:
    existing_perm = db.query(Permission).filter(Permission.name == perm_data.name).first()
    if existing_perm:
        return PermissionResponse(id=existing_perm.id, name=existing_perm.name)

    permission = Permission(name=perm_data.name)
    db.add(permission)
    db.commit()
    db.refresh(permission)

    return PermissionResponse(id=permission.id, name=permission.name)


def list_permissions(db: Session) -> List[PermissionResponse]:
    permissions = db.query(Permission).all()
    return [PermissionResponse(id=p.id, name=p.name) for p in permissions]
