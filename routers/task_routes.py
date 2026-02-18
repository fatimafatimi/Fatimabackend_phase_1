from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.task import Task
from models.project import Project
from typing import List
from schemas.task_schema import TaskCreate, TaskResponse, TaskUpdate

task_router = APIRouter (prefix="/tasks", tags=["Tasks"])

@router.post("/project/{project_id}/tasks", response_model=TaskResponse)
def create_task(project_id: int, task:TaskCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = Task(
        title= task.title,
        description= task.description,
        status="pending", 
        project_id = project_id
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task

@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
def get_all(project_id: int , db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.project_id == project_id).all()


@router.put("/tasks/{task_id}", response_model= TaskResponse)
def update_task(task_id:int, task:TaskUpdate, db: Session = Depends (get_db)):
    db_task = db.query(Task).filter (Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail= "Task not found")
    
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
        
    db.commit()
    db.refresh(db_task)
    
    return db_task
    

@router.delete("/tasks/{task_id}")
def delete_project(task_id: int , db: Session = Depends(get_db)):
    db_task= db.query (Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}
