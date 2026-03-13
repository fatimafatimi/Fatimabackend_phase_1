from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Request schema for creating a plan
class PlanCreate(BaseModel):
    name: str
    price: float
    billing_cycle: str  
    stripe_price_id: str
    description: Optional[str] = None
    
    
class PlanUpdate(BaseModel):
    name: str
    price: float
    billing_cycle: str
    

# Response schema for returning a plan
class PlanResponse(BaseModel):
    id: int
    name: str
    price: float
    billing_cycle: str
    stripe_price_id: str
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True  