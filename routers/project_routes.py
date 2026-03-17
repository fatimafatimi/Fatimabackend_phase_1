from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.project_schema import ProjectCreate, ProjectResponse
from handler.project_handler import (
    create_project,
    get_all_projects,
    get_project_by_id,
    delete_project,
    update_project
)
from dependencies.auth import get_current_user, require_admin, require_project_owner
from models.user import User

project_router = APIRouter(prefix="/projects", tags=["Projects"])

    # Admins can create projects for anyone.
    # Normal users can create projects for themselves only.
    # Owner of project is automatically set to current_user.
    
# create Project
@project_router.post("/", response_model=ProjectResponse)
def create_project_route(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_project(db, project, current_user)




    # Admin sees all projects.
    # Normal users see only their own projects.
    
# Get all projects
@project_router.get("/", response_model=list[ProjectResponse])
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = get_all_projects(db)
    if current_user.role != "admin":
        projects = [p for p in projects if p.owner_id == current_user.id]
    return projects




    # Admin can view any project.
    # Normal users can view only their own project.
    
# Get Project by id
@project_router.get("/{id}", response_model=ProjectResponse)
def get_project_by_id_route(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if current_user.role != "admin" and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return project



    # Admin can update any project.
    # Normal users can update only their own projects.
    # Ownership and admin check handled in `require_project_owner`.

# Update Project
@project_router.put("/{id}", response_model=ProjectResponse)
def update_project_route(
    id: int,
    project: ProjectCreate,
    db: Session = Depends(get_db),
    project_obj = Depends(require_project_owner)
):
    return update_project(db, id, project, project_obj.owner)


    # Admin can delete any project.
    # Normal users can delete only their own projects.
    # Ownership and admin check handled in `require_project_owner`.

# Delete Project
@project_router.delete("/{id}")
def delete_project_route(
    id: int,
    db: Session = Depends(get_db),
    project_obj = Depends(require_project_owner)
):
    return delete_project(db, id, project_obj.owner)