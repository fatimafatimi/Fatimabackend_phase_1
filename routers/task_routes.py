# routers/task_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from handler.task_handler import create_task, get_tasks_by_project, update_task, delete_task
from dependencies.auth import get_current_user
from models.user import User
from dependencies.permissions import require_permission

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Create Tasks
@task_router.post("/{project_id}", response_model=TaskResponse)
def create_task_route(
    project_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("create_task"))
):
    return create_task(db, project_id, task, current_user)

# GET tasks by project
@task_router.get("/projects/{project_id}", response_model=List[TaskResponse])
def get_tasks_by_project_route(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("view_tasks"))
):
    return get_tasks_by_project(db, project_id, current_user)


# Update Task
@task_router.put("/{task_id}", response_model=TaskResponse)
def update_task_route(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("update_task"))
):
    return update_task(db, task_id, task, current_user)



# Delete Task
@task_router.delete("/{task_id}")
def delete_task_route(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("delete_task"))
):
    return delete_task(db, task_id, current_user)