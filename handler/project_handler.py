from models.project import Project
from models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import Depends, status
from dependencies.auth import get_user

# create project
def create_project(db: Session, project, current_user: User = Depends(get_user)):
    new_project = Project(
        name=project.name,
        description=project.description,
        owner_id=current_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project

# update project
def update_project(
    db: Session,
    project_id: int,
    project_data,
    current_user: User = Depends(get_user)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user.role != "admin" and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this project"
        )

    project.name = project_data.name
    project.description = project_data.description

    db.commit()
    db.refresh(project)

    return project

# get all projects
def get_all_projects(db: Session):
    return db.query(Project).all()

# project by id
def get_project_by_id(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

# del project
def delete_project(
    db: Session,
    project_id: int,
    current_user: User = Depends(get_user)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user.role != "admin" and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this project"
        )

    db.delete(project)
    db.commit()

    return {"message": "Project deleted"}