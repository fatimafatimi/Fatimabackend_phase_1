from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models.user import User
from utils.jwt_handler import decode_access_token
from passlib.context import CryptContext
from models.role import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_access_token(token)  
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User)\
             .options(joinedload(User.role).joinedload(Role.permissions))\
             .filter(User.email == email)\
             .first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user