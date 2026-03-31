from pydantic import BaseModel
from typing import Optional
from schemas.role import RoleResponse
 
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    company_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: Optional[RoleResponse]
    
    class Config:
        from_attributes = True