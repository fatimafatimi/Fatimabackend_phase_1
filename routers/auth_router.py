# routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from handler.user_handler import login_user
from models.user import User
from utils.otp_utils import verify_otp, create_otp, check_otp_verified, consume_verified_otp
from utils.security import hash_password
from utils.email_service import send_email
import dns.resolver
import smtplib
import socket

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


def email_exists_in_real_world(email: str) -> bool:
    """
    Returns True if the email address likely exists in the real world.
    Checks:
      1. DNS MX record exists for the domain
      2. SMTP RCPT TO check confirms the mailbox (best-effort)
    """
    try:
        domain = email.split("@")[-1]

        # Step 1: Check MX record
        mx_records = dns.resolver.resolve(domain, "MX")
        if not mx_records:
            return False

        # Step 2: Pick the mail server with lowest priority
        mx_host = str(sorted(mx_records, key=lambda r: r.preference)[0].exchange).rstrip(".")

        # Step 3: SMTP handshake to verify the mailbox
        with smtplib.SMTP(timeout=10) as smtp:
            smtp.connect(mx_host, 25)
            smtp.helo(socket.getfqdn())
            smtp.mail("")           # empty sender is standard for probing
            code, _ = smtp.rcpt(email)
            smtp.quit()
            return code == 250      # 250 = mailbox exists

    except Exception:
        # Any failure (DNS error, SMTP rejection, timeout, etc.)
        # means we can't confirm it exists → treat as non-existent
        return False


@auth_router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(db, form_data.username, form_data.password)


@auth_router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = create_otp(db, user.id, "password_reset")

    # ✅ Now checks real-world existence, not just domain name
    if email_exists_in_real_world(email):
        # Real, existing email → send via SMTP
        send_email(
            to=user.email,
            subject="Password Reset OTP",
            template_name="otp_email.html",
            context={"otp": otp.otp_code}
        )
    else:
        # Email doesn't exist in real world (fake/test) → print to console
        print(f"[DEV] Password reset OTP for {user.email}: {otp.otp_code}")

    return {"message": "OTP sent. Check your email or console if testing."}


@auth_router.post("/verify-reset-otp")
def verify_reset_otp(email: str, otp_code: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    is_valid, message = verify_otp(db, user.id, otp_code, "password_reset")
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    return {"message": "OTP verified. You can now reset your password."}


@auth_router.post("/reset-password")
def reset_password(email: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not check_otp_verified(db, user.id, "password_reset"):
        raise HTTPException(
            status_code=403,
            detail="You must verify your OTP first before resetting your password"
        )

    user.hashed_password = hash_password(new_password)
    consume_verified_otp(db, user.id, "password_reset")
    db.commit()

    print(f"Password for {user.email} has been reset successfully.")
    return {"message": "Password updated successfully"}