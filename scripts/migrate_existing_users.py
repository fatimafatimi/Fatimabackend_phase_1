# scripts/migrate_existing_users.py
from database import SessionLocal
from models.tenant import Tenant
from models.user import User
from models.role import Role
from models.permission import Permission

ADMIN_PERMISSIONS = [
    "create_project", "update_project", "view_all_projects", "view_project", "delete_project",
    "create_task", "view_tasks", "update_task", "delete_task",
    "manage_roles", "view_roles", "manage_permissions",
]

USER_PERMISSIONS = [
    "create_project", "update_project", "view_project", "delete_project",
    "create_task", "view_tasks", "update_task", "delete_task",
]

def seed_permissions_for_tenant(db, tenant_id):
    all_names = set(ADMIN_PERMISSIONS + USER_PERMISSIONS)
    perm_map = {}

    for name in all_names:
        existing = db.query(Permission).filter(
            Permission.name == name,
            Permission.tenant_id == tenant_id
        ).first()
        if not existing:
            p = Permission(name=name, tenant_id=tenant_id)
            db.add(p)
            db.flush()
            perm_map[name] = p
        else:
            perm_map[name] = existing

    admin_role = db.query(Role).filter(Role.name == "admin", Role.tenant_id == tenant_id).first()
    if not admin_role:
        admin_role = Role(name="admin", tenant_id=tenant_id)
        db.add(admin_role)
        db.flush()
    admin_role.permissions = [perm_map[p] for p in ADMIN_PERMISSIONS]

    user_role = db.query(Role).filter(Role.name == "user", Role.tenant_id == tenant_id).first()
    if not user_role:
        user_role = Role(name="user", tenant_id=tenant_id)
        db.add(user_role)
        db.flush()
    user_role.permissions = [perm_map[p] for p in USER_PERMISSIONS]

    db.commit()
    print(f"  ✓ Tenant {tenant_id}: permissions seeded, roles updated")
    return admin_role, user_role


def run():
    db = SessionLocal()
    try:
        # 1. Make sure default tenant exists
        default_tenant = db.query(Tenant).filter(Tenant.name == "Default").first()
        if not default_tenant:
            default_tenant = Tenant(name="Default")
            db.add(default_tenant)
            db.commit()
            db.refresh(default_tenant)
            print(f"Created default tenant id={default_tenant.id}")

        # 2. Seed ALL tenants (including existing ones)
        all_tenants = db.query(Tenant).all()
        for tenant in all_tenants:
            print(f"Seeding tenant: {tenant.name} (id={tenant.id})")
            seed_permissions_for_tenant(db, tenant.id)

        # 3. Fix users with no tenant → assign to default tenant
        users_no_tenant = db.query(User).filter(User.tenant_id == None).all()
        for u in users_no_tenant:
            u.tenant_id = default_tenant.id
            user_role = db.query(Role).filter(
                Role.name == "user",
                Role.tenant_id == default_tenant.id
            ).first()
            if user_role and not u.role_id:
                u.role_id = user_role.id
            print(f"  Migrated user: {u.email} → default tenant")
        db.commit()

        # 4. Fix users whose role has no permissions (reassign correct role)
        all_users = db.query(User).filter(User.is_super_admin == False).all()
        for u in all_users:
            if not u.role or len(u.role.permissions) == 0:
                expected_role_name = "admin" if (u.role and u.role.name == "admin") else "user"
                correct_role = db.query(Role).filter(
                    Role.name == expected_role_name,
                    Role.tenant_id == u.tenant_id
                ).first()
                if correct_role:
                    u.role_id = correct_role.id
                    print(f"  Fixed role for user: {u.email} → {expected_role_name}")
        db.commit()

        print("\n Migration complete.")
    finally:
        db.close()

if __name__ == "__main__":
    run()