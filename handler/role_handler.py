from database import SessionLocal
from models.role import Role
from models.permission import Permission
from schemas.role import RoleCreate, RoleResponse
from typing import Optional, List
from sqlalchemy.orm import Session

db = SessionLocal()

# ----------------------
# CREATE ROLE
# ----------------------
def create_role(db: Session, name: str) -> Role:
    """
    Create a new role if it does not exist.
    """
    existing_role = db.query(Role).filter(Role.name == name).first()
    if existing_role:
        return existing_role  # or raise an exception if needed
    
    new_role = Role(name=name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


# ----------------------
# GET ROLE BY ID
# ----------------------
def get_role_with_permissions(db: Session, role_id: int) -> dict:
    """
    Fetch a role by ID along with its permissions.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise Exception(f"Role with ID '{role_id}' not found")
    
    return {
        "id": role.id,
        "name": role.name,
        "permissions": [perm.name for perm in role.permissions]
    }


# ----------------------
# LIST ALL ROLES
# ----------------------
def list_roles(db: Session) -> List[dict]:
    """
    List all roles with their permissions.
    """
    roles = db.query(Role).all()
    result = []
    for role in roles:
        result.append({
            "id": role.id,
            "name": role.name,
            "permissions": [perm.name for perm in role.permissions]
        })
    return result


# ----------------------
# ASSIGN PERMISSIONS TO ROLE
# ----------------------
def assign_permissions_to_role(db: Session, role_id: int, permission_names: List[str]) -> Role:
    """
    Assign permissions to a role using role_id.
    """
    # fetch role by ID
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise Exception(f"Role with ID '{role_id}' not found")

    # fetch permissions by name
    permissions = db.query(Permission).filter(Permission.name.in_(permission_names)).all()
    if not permissions:
        raise Exception("No valid permissions found for the given names")

    # assign permissions
    role.permissions = permissions
    db.commit()
    db.refresh(role)
    return role