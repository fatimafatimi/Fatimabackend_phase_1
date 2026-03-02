from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from handler.project_handler import (
    create_project,
    update_project,
    get_all_projects,
    get_project_by_id,
    delete_project
)
from database import get_db
from dependencies.permissions import require_permission

project_router = APIRouter(prefix="/projects", tags=["Projects"])


@project_router.post("/")
def create_project_route(
    project_data,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("create_project"))
):
    return create_project(db, project_data, current_user)


@project_router.put("/{project_id}")
def update_project_route(
    project_id: int,
    project_data,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("update_project"))
):
    return update_project(db, project_id, project_data, current_user)


@project_router.get("/")
def list_projects_route(
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("view_all_projects"))
):
    return get_all_projects(db)


@project_router.get("/{project_id}")
def get_project_route(
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("view_project"))
):
    return get_project_by_id(db, project_id)


@project_router.delete("/{project_id}")
def delete_project_route(
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("delete_project"))
):
    return delete_project(db, project_id, current_user)
