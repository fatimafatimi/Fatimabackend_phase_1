from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from database import get_db
from schemas.user_schema import UserLogin, UserResponse, UserRegister
from utils.security import get_current_user
from handler.user_handler import create_user, login_user

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/register", response_model=UserResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    return create_user(db, user)


@user_router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    return login_user(db, username, password)


@user_router.get("/me", response_model=UserResponse)
def read_me(current_user=Depends(get_current_user)):
    return current_user
