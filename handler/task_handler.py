from models.task import Task
from models.project import Project
from sqlalchemy.orm import Session
from fastapi import HTTPException


def create_task(db: Session, project_id: int, task):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = Task(
        title=task.title,
        description=task.description,
        status="pending",
        project_id=project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_tasks_by_project(db: Session, project_id: int):
    return db.query(Task).filter(Task.project_id == project_id).all()


def update_task(db: Session, task_id: int, task):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()

    return {"message": "Task deleted"}
