# schemas/task_schema.py
from pydantic import BaseModel, field_validator
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_user_id: Optional[int] = None

    @field_validator("assigned_user_id", mode="before")
    @classmethod
    def reject_zero_user_id(cls, v):
        return None if v == 0 else v

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    assigned_user_id: Optional[int] = None

    @field_validator("assigned_user_id", mode="before")
    @classmethod
    def reject_zero_user_id(cls, v):
        return None if v == 0 else v

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    project_id: int
    tenant_id: int

    class Config:
        from_attributes = True