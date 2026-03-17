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
<<<<<<< HEAD
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
<<<<<<< HEAD
    
    return {"message" : "Login Successful"}
=======

    token_expires = timedelta(minutes=30)
    token = create_access_token({"sub": db_user.email}, expires_delta=token_expires)
    return {"access_token": token, "token_type": "bearer"}
=======
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    return login_user(db, username, password)
>>>>>>> origin/handler_config


@user_router.get("/me", response_model=UserResponse)
def read_me(current_user=Depends(get_current_user)):
    return current_user
>>>>>>> jwt_auth
