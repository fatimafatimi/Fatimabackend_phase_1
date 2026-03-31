# handler/project_handler.py
from models.project import Project
from models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def create_project(db: Session, project_data, current_user: User):
    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=current_user.id,
        tenant_id=current_user.tenant_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def update_project(db: Session, project_id: int, project_data, current_user: User):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if (
        not current_user.is_super_admin
        and current_user.role.name != "admin"
        and project.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this project"
        )

    project.name = project_data.name
    project.description = project_data.description
    db.commit()
    db.refresh(project)
    return project


def get_all_projects(db: Session, current_user: User):
    query = db.query(Project)
    if not current_user.is_super_admin:
        query = query.filter(Project.tenant_id == current_user.tenant_id)
    return query.all()


def get_project_by_id(db: Session, project_id: int, current_user: User):
    query = db.query(Project).filter(Project.id == project_id)
    if not current_user.is_super_admin:
        query = query.filter(Project.tenant_id == current_user.tenant_id)
    project = query.first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def delete_project(db: Session, project_id: int, current_user: User):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if (
        not current_user.is_super_admin
        and current_user.role.name != "admin"
        and project.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this project"
        )

    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}