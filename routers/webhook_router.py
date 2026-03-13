from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import stripe

from database import get_db
from utils.stripe_service import verify_webhook
from models.user import User
from models.plan import Plan
from models.subscription import Subscription
from models.payment import Payment

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"]
)

@router.post("/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    event = verify_webhook(payload, sig_header)

    if event.type != "checkout.session.completed":
        print(f"Unhandled event: {event.type}")
        return {"status": "ignored"}

    session = event.data.object

    try:
        customer_email = session.get("customer_email") or session.get("customer_details", {}).get("email")
        if not customer_email:
            return {"status": "no_email"}

        user = db.query(User).filter(User.email == customer_email).first()
        if not user:
            return {"status": "user_not_found"}


        plan_id = session.get("metadata", {}).get("plan_id")
        if not plan_id:
            return {"status": "no_plan_id"}

        plan_id = int(plan_id)

      
        stripe_subscription_id = session.get("subscription")

        if not stripe_subscription_id:
            stripe_session = stripe.checkout.Session.retrieve(session.id)
            stripe_subscription_id = stripe_session.subscription

        if not stripe_subscription_id:
            return {"status": "no_subscription_id"}

  
        existing_sub = db.query(Subscription).filter(
            Subscription.stripe_subscription_id == stripe_subscription_id
        ).first()

        if existing_sub:
            return {"status": "subscription_exists"}

        
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=30)

        subscription = Subscription(
            user_id=user.id,
            plan_id=plan_id,
            status="active",
            start_date=start_date,
            end_date=end_date,
            stripe_subscription_id=stripe_subscription_id
        )

        db.add(subscription)
        db.commit()
        db.refresh(subscription)

        
        payment_intent = session.get("payment_intent") or "subscription_payment"

        payment = Payment(
            user_id=user.id,
            subscription_id=subscription.id,
            amount=(session.get("amount_total") or 0) / 100,
            status="succeeded",
            stripe_payment_intent=payment_intent,
            payment_method="card"
        )

        db.add(payment)
        db.commit()

        print(f"Subscription and payment saved for {user.email}")

    except Exception as e:
        db.rollback()
        print(f"Webhook error: {e}")
        return {"status": "error"}

    return {"status": "success"}