from database import SessionLocal
from models.role import Role
from models.permission import Permission

db = SessionLocal()

# Define all permissions
permission_names = [
    "create_user",
    "register_user",
    "create_project",
    "update_project",
    "delete_project",
    "view_all_projects",
    "create_role",
    "assign_permission",
    "create_permission",
    "delete_task",
    "update_task",
    "manage_roles",      
    "manage_permissions"
]

# Create permissions if they don't exist
for name in permission_names:
    perm = db.query(Permission).filter_by(name=name).first()
    if not perm:
        db.add(Permission(name=name))

db.commit()

# Fetch all permissions
all_permissions = db.query(Permission).all()

# Get or create admin role
admin_role = db.query(Role).filter_by(name="admin").first()
if not admin_role:
    admin_role = Role(name="admin")
    db.add(admin_role)
    db.commit()

# Assign ALL permissions to admin (overwrite existing)
admin_role.permissions = all_permissions
db.commit()

db.close()

print("RBAC seeding completed successfully.")