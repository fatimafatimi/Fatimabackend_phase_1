from pydantic import BaseModel

class PermissionCreate(BaseModel):
    name: str

class PermissionResponse(BaseModel):
    id: int
    name: str
    tenant_id: int
    
    class Config:
        # orm_mode = True
        from_attributes = True
