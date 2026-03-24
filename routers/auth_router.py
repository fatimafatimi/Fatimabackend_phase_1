from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db

from handler.user_handler import login_user
from models.user import User

from utils.otp_utils import verify_otp, create_otp
from utils.email_service import send_email
from utils.security import hash_password


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


# LOGIN
@auth_router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(db, form_data.username, form_data.password)


# EMAIL VERIFICATION
@auth_router.post("/verify-email")
def verify_email(user_id: int, otp_code: str, db: Session = Depends(get_db)):

    is_valid, message = verify_otp(db, user_id, otp_code, "email_verification")

    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_email_verified = True
    db.commit()

    
    send_email(
        to=user.email,
        subject="Welcome to Mini PMS",
        template_name="welcome_email.html",
        context={"name": user.username}
    )

    return {"message": "Email verified successfully"}


# FORGOT PASSWORD
@auth_router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = create_otp(db, user.id, "password_reset")

    send_email(
        to=user.email,
        subject="Password Reset OTP",
        template_name="otp_email.html",
        context={"otp": otp.otp_code}
    )

    return {"message": "OTP sent"}


# VERIFY RESET OTP
@auth_router.post("/verify-reset-otp")
def verify_reset_otp(user_id: int, otp_code: str, db: Session = Depends(get_db)):

    is_valid, message = verify_otp(db, user_id, otp_code, "password_reset")

    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    return {"message": "OTP verified"}


# RESET PASSWORD
@auth_router.post("/reset-password")
def reset_password(user_id: int, new_password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(new_password)
    db.commit()

    
    send_email(
        to=user.email,
        subject="Password Changed",
        template_name="password_changed.html",
        context={"name": user.username}
    )

    return {"message": "Password updated successfully"}