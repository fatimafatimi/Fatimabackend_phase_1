from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.project_schema import ProjectCreate, ProjectResponse
from handler.project_handler import (
    create_project,
    get_all_projects,
    get_project_by_id,
    delete_project
)

project_router = APIRouter(prefix="/projects", tags=["Projects"])


@project_router.post("/", response_model=ProjectResponse)
def create_project_route(project: ProjectCreate, db: Session = Depends(get_db)):
    return create_project(db, project)


@project_router.get("/", response_model=list[ProjectResponse])
def get_project(db: Session = Depends(get_db)):
    return get_all_projects(db)


@project_router.get("/{id}", response_model=ProjectResponse)
def get_projectbyid(id: int, db: Session = Depends(get_db)):
    return get_project_by_id(db, id)


@project_router.delete("/{id}")
def delete_project_route(id: int, db: Session = Depends(get_db)):
    return delete_project(db, id)
