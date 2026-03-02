from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from database import get_db
from schemas.user_schema import UserLogin, UserResponse, UserRegister
from handler.user_handler import create_user, login_user
from dependencies.auth import require_admin, get_user
from models.user import User
from dependencies.auth import get_current_user

user_router = APIRouter(prefix="/users", tags=["Users"])

# Admin-only route for creating users
@user_router.post("/register", response_model=UserResponse)
def register(user: UserRegister, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    return create_user(db, user, current_user)


# Login route
@user_router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    return login_user(db, username, password)


# Get current user info
@user_router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user