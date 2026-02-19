from models.project import Project
from models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException


def create_project(db: Session, project):
    owner = db.query(User).filter(User.id == project.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")

    new_project = Project(
        name=project.name,
        description=project.description,
        owner_id=project.owner_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


def get_all_projects(db: Session):
    return db.query(Project).all()


def get_project_by_id(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


def delete_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return {"message": "Project deleted"}
