# routers/ payment_router.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.plan import Plan
from models.user import User
from models.payment import Payment
from models.subscription import Subscription
from schemas.payment_schema import PaymentCreateResponse, PaymentResponse
from utils.stripe_service import create_checkout_session
from dependencies.auth import get_current_user, require_admin
from utils.email_service import send_payment_failed_email

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

#  Create Stripe Checkout Session
@router.post("/create-checkout-session", response_model=PaymentCreateResponse)
def create_payment_session(
    plan_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role and current_user.role.name == "admin":
        raise HTTPException(status_code=403, detail="Admins cannot purchase plans")

    active_subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == "active"
    ).first()
    if active_subscription:
        raise HTTPException(status_code=400, detail="You already have an active subscription")

    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    if not plan.stripe_price_id:
        raise HTTPException(status_code=400, detail="Plan not linked to Stripe Price ID")

    # Try creating Stripe checkout session
    try:
        session = create_checkout_session(
            customer_email=current_user.email,
            price_id=plan.stripe_price_id,
            plan_id=plan.id
        )
    except Exception as e:
        # Send payment failed email in background
        background_tasks.add_task(
            send_payment_failed_email,
            user_email=current_user.email
        )
        raise HTTPException(status_code=400, detail=f"Payment failed: {str(e)}")

    return PaymentCreateResponse(checkout_url=session.url)


#  Get Payment History
@router.get("/my-payments", response_model=List[PaymentResponse])
def get_my_payments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    payments = db.query(Payment).filter(
        Payment.user_id == current_user.id
    ).all()
    return payments


# Get all Payments
@router.get("/", response_model=List[PaymentResponse])
def get_all_payments(
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    payments = db.query(Payment).all()
    return payments



