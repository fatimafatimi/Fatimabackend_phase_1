# utils/security.py
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from utils.jwt_handler import decode_access_token
from passlib.context import CryptContext


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)




def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = decode_access_token(token)
    user = db.query(User).filter(User.email == payload["sub"]).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user