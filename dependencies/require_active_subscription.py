from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.subscription import Subscription
from models.user import User
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.id == 1).first()  
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

def require_active_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id)
        .order_by(Subscription.end_date.desc())
        .first()
    )

    if not subscription or subscription.status != "active":
        raise HTTPException(status_code=403, detail="Active subscription required")

    return subscription 