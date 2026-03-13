from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PaymentCreateResponse(BaseModel):
    checkout_url: str

class PaymentResponse(BaseModel):
    id: int
    user_id: int
    subscription_id: int
    amount: float
    status: str
    stripe_payment_intent: str
    payment_method: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True