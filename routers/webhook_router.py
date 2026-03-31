# routers/ webhook_router.py
from fastapi import APIRouter, Request, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import stripe
from database import get_db
from utils.stripe_service import verify_webhook
from models.user import User
from models.plan import Plan
from models.subscription import Subscription
from models.payment import Payment
from utils.email_service import (
    send_payment_success_email,
    send_payment_failed_email,
    send_tenant_admin_payment_notification
)

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = verify_webhook(payload, sig_header)
    except Exception as e:
        print(f"Webhook signature verification failed: {e}")
        return {"status": "invalid_signature"}

    session = event.data.object

    # ── failed payments ──────────────────────────────────────
    if event.type in ["payment_intent.payment_failed", "checkout.session.async_payment_failed"]:
        customer_email = None

        if event.type == "checkout.session.async_payment_failed":
            customer_email = session.get("customer_email") or session.get("customer_details", {}).get("email")

        if event.type == "payment_intent.payment_failed":
            payment_method = session.get("last_payment_error", {}).get("payment_method", {})
            billing = payment_method.get("billing_details", {})
            customer_email = billing.get("email")

        if customer_email:
            background_tasks.add_task(send_payment_failed_email, user_email=customer_email)

        print(f"Payment failed for {customer_email}")
        return {"status": "payment_failed"}

    if event.type != "checkout.session.completed":
        print(f"Ignored event type: {event.type}")
        return {"status": "ignored"}

    # ── successful payment ───────────────────────────────────
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
        plan = db.query(Plan).filter(Plan.id == plan_id).first()
        if not plan:
            return {"status": "plan_not_found"}

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
        db.refresh(payment)

        print(f"Subscription and payment saved for {user.email}")

        amount_str = f"{payment.amount} USD"

        # email to user — with login credentials
        background_tasks.add_task(
            send_payment_success_email,
            user_email=user.email,
            plan_name=plan.name,
            amount=amount_str,
            login_email=user.email,
            password="[your registered password]"  # we never store plain text — remind them
        )

        # email to tenant admin — notify that their user paid
        tenant_admin = db.query(User).filter(
            User.tenant_id == user.tenant_id,
            User.role.has(name="admin")  # find the admin of same tenant
        ).first()

        if tenant_admin:
            background_tasks.add_task(
                send_tenant_admin_payment_notification,
                admin_email=tenant_admin.email,
                admin_username=tenant_admin.username,
                user_email=user.email,
                username=user.username,
                plan_name=plan.name
            )

    except Exception as e:
        db.rollback()
        print(f"Webhook processing error: {e}")
        return {"status": "error"}

    return {"status": "success"}