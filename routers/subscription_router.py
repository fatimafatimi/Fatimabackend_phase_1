from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models.subscription import Subscription
from models.user import User
from dependencies import get_current_user
from utils.stripe_service import cancel_subscription
from utils.email_service import send_subscription_cancelled_email

router = APIRouter(
    prefix="/subscription",
    tags=["Subscriptions"]
)


# Get Current User Subscription
@router.get("/me")
def get_my_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).order_by(Subscription.created_at.desc()).first()

    if not subscription:
        raise HTTPException(status_code=404, detail="No subscription found")

    return {
        "id": subscription.id,
        "plan_id": subscription.plan_id,
        "status": subscription.status,
        "start_date": subscription.start_date,
        "end_date": subscription.end_date
    }


# Cancel Subscription
@router.post("/cancel")
def cancel_my_subscription(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == "active"
    ).first()

    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription found")

    if not subscription.stripe_subscription_id:
        raise HTTPException(status_code=400, detail="Cannot cancel: Stripe subscription ID not found")

    try:
        cancel_subscription(subscription.stripe_subscription_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Stripe cancellation failed: {str(e)}")

    subscription.status = "cancelled"
    subscription.end_date = datetime.utcnow()
    db.commit()
    db.refresh(subscription)

    # Send cancellation email in background
    background_tasks.add_task(
        send_subscription_cancelled_email,
        subscription.user.email
    )

    return {
        "message": "Subscription cancelled successfully",
        "subscription_id": subscription.id,
        "plan_id": subscription.plan_id
    }


# Get Subscription Status
@router.get("/status")
def get_subscription_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).order_by(Subscription.created_at.desc()).first()

    if not subscription:
        return {"status": "none"}

    return {"status": subscription.status, "end_date": subscription.end_date}




