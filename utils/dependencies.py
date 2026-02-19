from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from utils.security import get_current_user
from models.user import User

# Shortcut dependency to get current user
def get_user(current_user: User = Depends(get_current_user)):
    return current_user

# Shortcut dependency to get DB session
def get_db_session(db: Session = Depends(get_db)):
    return db
