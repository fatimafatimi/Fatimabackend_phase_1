from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user_schema import UserLogin, UserResponse, UserRegister
from utils.security import hash_password, verify_password, get_current_user
from utils.jwt_handler import create_access_token
from datetime import timedelta

from fastapi import Form 

user_router = APIRouter(prefix="/users", tags=["Users"])

# Register a new user
@user_router.post("/register", response_model=UserResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@user_router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == username).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token_expires = timedelta(minutes=30)
    token = create_access_token({"sub": db_user.email}, expires_delta=token_expires)
    return {"access_token": token, "token_type": "bearer"}


# Get current logged-in user
@user_router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

