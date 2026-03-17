from fastapi import APIRouter, Depends
from dependencies.require_active_subscription import require_active_subscription
from dependencies.auth import get_current_user
from database import get_db
from models.user import User
from sqlalchemy.orm import Session
from models.subscription import Subscription

router = APIRouter()

@router.get("/premium-content")
def get_premium_content(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == "active"
    ).order_by(Subscription.created_at.desc()).first()

    if not subscription:
        raise HTTPException(status_code=403, detail="Active subscription required")

    return {"message": "Welcome to premium content!"}