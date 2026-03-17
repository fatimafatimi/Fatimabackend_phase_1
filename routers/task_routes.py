from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from handler.task_handler import create_task, get_tasks_by_project, update_task, delete_task
from dependencies.auth import get_current_user, require_task_owner
from models.user import User

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


    # Admin can add tasks to any project.
    # Normal users can add tasks only to their own projects.

# Create Tasks
@task_router.post("/{project_id}", response_model=TaskResponse)
def create_task_route(
    project_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_task(db, project_id, task, current_user)



    # Admin can view all tasks of any project.
    # Normal users can view tasks only for their own projects.

# Get all tasks
@task_router.get("/projects/{project_id}", response_model=List[TaskResponse])
def get_tasks_by_project_route(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_tasks_by_project(db, project_id, current_user)




    # Admin can update any task.
    # Normal users can update only tasks belonging to their own projects.
    # Ownership/admin check is handled in `require_task_owner`.

# Update Task
@task_router.put("/{task_id}", response_model=TaskResponse)
def update_task_route(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_task(db, task_id, task, current_user)



    # Admin can delete any task.
    # Normal users can delete only tasks belonging to their own projects.
    # Ownership/admin check is handled in `require_task_owner`.
    
# Delete Task
@task_router.delete("/{task_id}")
def delete_task_route(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_task(db, task_id, current_user)