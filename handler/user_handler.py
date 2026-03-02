from models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.security import hash_password, verify_password
from utils.jwt_handler import create_access_token
from datetime import timedelta
from fastapi import Depends,status
from dependencies.auth import require_admin, get_user
from models.role import Role

def create_user(db: Session, user, current_user: User):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    role = db.query(Role).filter(Role.name == "user").first()
    if not role:
        raise HTTPException(status_code=500, detail="Default user role not found")

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role_id=role.id  
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login_user(db: Session, username: str, password: str):
    db_user = db.query(User).filter(User.email == username).first()

    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email, "role": db_user.role.name})

    return {"access_token": token, "token_type": "bearer"}
