# handler/user_handler.py
from models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.security import hash_password, verify_password
from utils.jwt_handler import create_access_token
from models.role import Role
from models.permission import Permission
from models.tenant import Tenant

# ─── Permission definitions ───

# Permissions given to the "admin" role in every tenant
ADMIN_PERMISSIONS = [
    "create_project",
    "update_project",
    "view_all_projects",
    "view_project",
    "delete_project",
    "create_task",
    "view_tasks",
    "update_task",
    "delete_task",
    "manage_roles",
    "view_roles",
    "manage_permissions",
]

# Permissions given to the "user" role in every tenant
USER_PERMISSIONS = [
    "create_project",
    "update_project",
    "view_project",
    "delete_project",
    "create_task",
    "view_tasks",
    "update_task",
    "delete_task",
]

# ─── Seed helper ───

def seed_tenant_roles_and_permissions(db: Session, tenant_id: int):
    all_permission_names = set(ADMIN_PERMISSIONS + USER_PERMISSIONS)

    perm_map = {}
    for perm_name in all_permission_names:
        perm = db.query(Permission).filter(
            Permission.name == perm_name,
            Permission.tenant_id == tenant_id
        ).first()
        if not perm:
            perm = Permission(name=perm_name, tenant_id=tenant_id)
            db.add(perm)
            db.flush()
        perm_map[perm_name] = perm

    admin_role = Role(name="admin", tenant_id=tenant_id)
    admin_role.permissions = [perm_map[p] for p in ADMIN_PERMISSIONS]
    db.add(admin_role)

    user_role = Role(name="user", tenant_id=tenant_id)
    user_role.permissions = [perm_map[p] for p in USER_PERMISSIONS]
    db.add(user_role)

    db.flush()
    return admin_role, user_role


# ─── Handlers ─────

def create_user(db: Session, user, current_user: User = None):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Determine tenant: caller's tenant if logged in, else default tenant
    if current_user:
        tenant_id = current_user.tenant_id
    else:
        default_tenant = db.query(Tenant).first()
        if not default_tenant:
            raise HTTPException(status_code=500, detail="Default tenant not found")
        tenant_id = default_tenant.id

    # Find the "user" role for this tenant
    role = db.query(Role).filter(
        Role.name == "user",
        Role.tenant_id == tenant_id
    ).first()

    # Safety: if somehow the role doesn't exist, create it with permissions
    if not role:
        _, role = seed_tenant_roles_and_permissions(db, tenant_id)
        db.commit()
        db.refresh(role)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role_id=role.id,
        tenant_id=tenant_id,
        is_email_verified=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(db: Session, username: str, password: str):
    db_user = db.query(User).filter(User.email == username).first()

    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({
        "sub": db_user.email,
        "role": db_user.role.name if db_user.role else "user",
        "tenant_id": db_user.tenant_id,
        "is_super_admin": db_user.is_super_admin,
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "tenant_id": db_user.tenant_id,
    }


def create_tenant_admin(db: Session, user, current_user: User):
    if not current_user.is_super_admin:
        raise HTTPException(status_code=403, detail="Only super admin can create tenant admins")

    if not user.company_name:
        raise HTTPException(status_code=400, detail="Company name is required")

    existing_tenant = db.query(Tenant).filter(Tenant.name == user.company_name).first()
    if existing_tenant:
        raise HTTPException(status_code=400, detail="Tenant already exists")

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create the tenant
    new_tenant = Tenant(name=user.company_name)
    db.add(new_tenant)
    db.flush()

    # Seed roles + permissions for this tenant
    admin_role, _ = seed_tenant_roles_and_permissions(db, new_tenant.id)
    db.commit()
    db.refresh(admin_role)

    # Create the tenant admin user
    new_admin = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role_id=admin_role.id,
        tenant_id=new_tenant.id,
        is_email_verified=True
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin