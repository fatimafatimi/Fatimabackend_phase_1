from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from database import get_db
from schemas.user_schema import UserLogin, UserResponse, UserRegister
from handler.user_handler import create_user, login_user
from dependencies.auth import require_admin
from models.user import User
from dependencies.auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from utils.otp_utils import create_otp
from utils.email_service import send_email


user_router = APIRouter(prefix="/users", tags=["Users"])
auth_router = APIRouter(prefix="/auth", tags=["Auth"])



@user_router.post("/register", response_model=UserResponse)
def register(user: UserRegister, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    return create_user(db, user, current_user)


@auth_router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(db, form_data.username, form_data.password)


# Get current user info
@user_router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@user_router.post("/resend-otp")
def resend_otp(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_email_verified:
        raise HTTPException(status_code=400, detail="User already verified")

    otp = create_otp(db, user.id, "email_verification")

    send_email(
        to=user.email,
        subject="Your OTP Code",
        template_name="otp_email.html",
        context={"otp": otp.otp_code}
    )

    return {"message": "OTP sent to your email"}