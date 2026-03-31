import stripe
from config.settings import settings
from fastapi import HTTPException

# Initialize Stripe
stripe.api_key = settings.STRIPE_API_KEY

# Create Stripe Checkout Session (Subscription)
def create_checkout_session(customer_email: str, price_id: str, plan_id: int):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            customer_email=customer_email,
            line_items=[{"price": price_id, "quantity": 1}],
            metadata={"plan_id": str(plan_id)},  
            success_url=f"{settings.STRIPE_SUCCESS_URL}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=settings.STRIPE_CANCEL_URL,
        )
        return session
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Stripe checkout session failed: {str(e)}")



# Cancel Stripe Subscription
def cancel_subscription(subscription_id: str):
    try:
        # ⚡ Use Stripe's cancel method properly
        subscription = stripe.Subscription.retrieve(subscription_id)
        if subscription.status == "canceled":
            raise HTTPException(status_code=400, detail="Subscription already cancelled")
        
        return stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=False  
        )
    except stripe.error.InvalidRequestError as e:
        raise HTTPException(status_code=400, detail=f"Stripe cancellation failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Stripe cancellation failed: {str(e)}")



# Retrieve Stripe Checkout Session
def retrieve_session(session_id: str):
    try:
        return stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Stripe session not found: {str(e)}")



# Verify Webhook
def verify_webhook(payload: bytes, sig_header: str):
    try:
        return stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Webhook signature verification failed")