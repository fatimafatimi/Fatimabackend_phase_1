from fastapi import Depends, HTTPException, status
from utils.security import get_current_user
from models.user import User

def require_permission(permission_name: str):
    def permission_dependency(current_user: User = Depends(get_current_user)):
        if not current_user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No role assigned"
            )

        permissions = [p.name for p in current_user.role.permissions]
        if permission_name not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
        return current_user
    return permission_dependency