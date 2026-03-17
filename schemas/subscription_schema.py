from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan_id: int
    status: str
    start_date: datetime
    end_date: Optional[datetime]
    stripe_subscription_id: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True