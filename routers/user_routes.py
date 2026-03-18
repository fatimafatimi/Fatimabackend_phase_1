from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from database import get_db
from schemas.user_schema import UserLogin, UserResponse, UserRegister
from handler.user_handler import create_user, login_user
from dependencies.auth import get_current_user, require_admin
from models.user import User
from fastapi.security import OAuth2PasswordRequestForm


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
