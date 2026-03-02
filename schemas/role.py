from pydantic import BaseModel
from typing import List, Optional
from schemas.permission import PermissionResponse


class RoleCreate(BaseModel):
    name: str
    permission_ids: Optional[List[int]] = []  


class RoleResponse(BaseModel):
    id: int
    name: str
    permissions: List[PermissionResponse]  
        
    class Config:
        from_attributes = True