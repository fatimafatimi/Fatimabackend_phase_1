# handler/task_handler.py
from models.task import Task
from models.project import Project
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from websocket.events import (
    task_created_event,
    task_updated_event,
    task_deleted_event
)


def _get_project_or_404(db: Session, project_id: int, current_user: User):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not current_user.is_super_admin and project.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def _can_modify_project(current_user: User, project: Project):
    if current_user.is_super_admin:
        return True
    if current_user.role and current_user.role.name == "admin":
        return True
    if project.owner_id == current_user.id:
        return True
    return False


async def create_task(db: Session, project_id: int, task, current_user: User):
    project = _get_project_or_404(db, project_id, current_user)

    if not _can_modify_project(current_user, project):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to add tasks to this project"
        )

    new_task = Task(
        title=task.title,
        description=task.description,
        status="pending",
        project_id=project_id,
        tenant_id=project.tenant_id,
        assigned_user_id=task.assigned_user_id 
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # WebSocket event
    try:
        await task_created_event(new_task)
    except Exception as e:
        print(f"WebSocket error: {e}")
    return new_task


def get_tasks_by_project(db: Session, project_id: int, current_user: User):
    project = _get_project_or_404(db, project_id, current_user)

    if not _can_modify_project(current_user, project):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view tasks for this project"
        )

    return db.query(Task).filter(Task.project_id == project_id).all()


async def update_task(db: Session, task_id: int, task, current_user: User):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = _get_project_or_404(db, db_task.project_id, current_user)

    if not _can_modify_project(current_user, project):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this task"
        )

    update_data = task.dict(exclude_unset=True)

   
    if "assigned_user_id" in update_data and update_data["assigned_user_id"] == 0:
        update_data["assigned_user_id"] = None

    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    #  WebSocket event
    try:
        await task_updated_event(db_task)
    except Exception as e:
        print(f"WebSocket error: {e}")
    return db_task    
        

async def delete_task(db: Session, task_id: int, current_user: User):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = _get_project_or_404(db, db_task.project_id, current_user)

    if not _can_modify_project(current_user, project):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this task"
        )

    project_id = db_task.project_id

    db.delete(db_task)
    db.commit()

    # 🔔 WebSocket event
    try:
        await task_deleted_event(task_id, project_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
    return {"message": "Task deleted"}    
    