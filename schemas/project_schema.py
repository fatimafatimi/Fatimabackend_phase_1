from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str 
    description: str
    owner_id: int
    
class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int
    
    class Config:
        orm_mode = True
