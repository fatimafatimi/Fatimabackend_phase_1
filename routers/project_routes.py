from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.project import Project
from schemas.project_schema import ProjectCreate, ProjectResponse

router = APIRouter (prefix="/projects", tags=["Projects"])

#Creating Project
@router.post("/", response_model = ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    owner= db.query(User).filter(User.id == project.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner Not Found")
    
    new_project = Project(
        name = project.name,
        description = project.description,
        owner_id = project.owner_id
    )
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

#Getting All Projects
@router.get("/", response_model=list[ProjectResponse])
def get_project(db: Session = Depends(get_db)):
    return db.query(Project).all()


#Getting Project by ID
@router.get("/{id}", response_model=ProjectResponse)
def get_projectbyid(id: int, db: Session = Depends(get_db)):
    project= db.query (Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


#Deleting Project
@router.delete("/{id}")
def delete_project(id: int , db: Session = Depends(get_db)):
    project= db.query (Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}
