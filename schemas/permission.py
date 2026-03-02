from pydantic import BaseModel

# Incoming data when creating a permission
class PermissionCreate(BaseModel):
    name: str

# Response data when sending permission info
class PermissionResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True