# handler/role_handler.py
from database import SessionLocal
from models.role import Role
from models.permission import Permission
from schemas.role import RoleCreate, RoleResponse
from typing import List
from sqlalchemy.orm import Session
from models.user import User
from fastapi import HTTPException

db = SessionLocal()

def create_role(db: Session, role_data: RoleCreate, current_user: User) -> RoleResponse:
    # Only tenant admins or super admins can create roles
    if not current_user.is_super_admin and current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create roles")

    # Check if role exists in tenant
    existing_role = db.query(Role).filter(
        Role.name == role_data.name,
        Role.tenant_id == current_user.tenant_id
    ).first()

    if existing_role:
        return RoleResponse.from_orm(existing_role)

    new_role = Role(name=role_data.name, tenant_id=current_user.tenant_id)

    # attach permissions if provided
    if role_data.permission_ids:
        permissions = db.query(Permission).filter(
            Permission.id.in_(role_data.permission_ids),
            Permission.tenant_id == current_user.tenant_id
        ).all()
        new_role.permissions = permissions

    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return RoleResponse.from_orm(new_role)


def get_role_with_permissions(db: Session, role_id: int, current_user: User) -> RoleResponse:
    query = db.query(Role).filter(Role.id == role_id)
    
    if not current_user.is_super_admin:
        query = query.filter(Role.tenant_id == current_user.tenant_id)
    
    role = query.first()
    if not role:
        raise HTTPException(status_code=404, detail=f"Role with ID '{role_id}' not found")

    return RoleResponse.from_orm(role)


def list_roles(db: Session, current_user: User) -> List[RoleResponse]:
    query = db.query(Role)
    if not current_user.is_super_admin:
        query = query.filter(Role.tenant_id == current_user.tenant_id)
    roles = query.all()
    return [RoleResponse.from_orm(r) for r in roles]


def assign_permissions_to_role(db: Session, role_id: int, permission_names: List[str], current_user: User) -> RoleResponse:
    query = db.query(Role).filter(Role.id == role_id)
    if not current_user.is_super_admin:
        query = query.filter(Role.tenant_id == current_user.tenant_id)
    role = query.first()

    if not role:
        raise HTTPException(status_code=404, detail=f"Role with ID '{role_id}' not found")

    permissions = db.query(Permission).filter(
        Permission.name.in_(permission_names)
    )
    if not current_user.is_super_admin:
        permissions = permissions.filter(Permission.tenant_id == current_user.tenant_id)
    permissions = permissions.all()

    if not permissions:
        raise HTTPException(status_code=404, detail="No valid permissions found for the given names")

    role.permissions = permissions
    db.commit()
    db.refresh(role)
    return RoleResponse.from_orm(role)