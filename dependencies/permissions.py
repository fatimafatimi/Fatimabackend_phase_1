# dependencies/permissions.py
from fastapi import Depends, HTTPException, status
from dependencies.auth import get_current_user
from models.user import User

def require_permission(permission_name: str):
    async def permission_dependency(current_user: User = Depends(get_current_user)):

        # Super admin bypasses all permission checks
        if current_user.is_super_admin:
            return current_user

        if not current_user.role or not current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No role or tenant assigned"
            )

        permissions = [p.name for p in current_user.role.permissions]

        if permission_name not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: '{permission_name}' required"
            )

        return current_user

    return permission_dependency