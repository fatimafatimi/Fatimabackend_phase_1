# dependencies/auth.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from utils.security import get_current_user as security_current_user
from models.user import User
from models.project import Project
from models.task import Task


def get_current_user(current_user: User = Depends(security_current_user)):
    return current_user


def require_admin(current_user: User = Depends(get_current_user)):
    # Super admin passes through always
    if current_user.is_super_admin:
        return current_user
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def require_project_owner(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    query = db.query(Project).filter(Project.id == project_id)
    if not current_user.is_super_admin:
        query = query.filter(Project.tenant_id == current_user.tenant_id)

    project = query.first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if (
        not current_user.is_super_admin
        and current_user.role.name != "admin"
        and project.owner_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="You do not have permission")

    return project


def require_task_owner(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    query = db.query(Project).filter(Project.id == task.project_id)
    if not current_user.is_super_admin:
        query = query.filter(Project.tenant_id == current_user.tenant_id)

    project = query.first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if (
        not current_user.is_super_admin
        and current_user.role.name != "admin"
        and project.owner_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="You do not have permission")

    return task