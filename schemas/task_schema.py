from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field (..., min_length =3)
    description: str
    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str