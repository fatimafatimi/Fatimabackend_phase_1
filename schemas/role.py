# from pydantic import BaseModel
# from typing import List, Optional
# from schemas.permission import PermissionResponse


# class RoleCreate(BaseModel):
#     name: str
#     permission_ids: Optional[List[int]] = []  


# class RoleResponse(BaseModel):
#     id: int
#     name: str
#     tenant_id: int
#     permissions: List[PermissionResponse]  
        
#     class Config:
#         # orm_mode = True
#         from_attributes = True

from pydantic import BaseModel
from typing import List, Optional
from schemas.permission import PermissionResponse

class RoleCreate(BaseModel):
    name: str
    permission_ids: Optional[List[int]] = []  

class RoleResponse(BaseModel):
    id: int
    name: str
    tenant_id: int
    permissions: List[PermissionResponse]  
        
    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode