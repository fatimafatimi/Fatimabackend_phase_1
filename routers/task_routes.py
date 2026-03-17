from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from schemas.task_schema import TaskCreate, TaskResponse, TaskUpdate
from handler.task_handler import create_task, get_tasks_by_project, update_task, delete_task

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_router.post("/{project_id}", response_model=TaskResponse)
def create_task_route(project_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, project_id, task)


@task_router.get("/projects/{project_id}", response_model=List[TaskResponse])
def get_all(project_id: int, db: Session = Depends(get_db)):
    return get_tasks_by_project(db, project_id)


@task_router.put("/{task_id}", response_model=TaskResponse)
def update_task_route(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return update_task(db, task_id, task)


@task_router.delete("/{task_id}")
def delete_task_route(task_id: int, db: Session = Depends(get_db)):
    return delete_task(db, task_id)
