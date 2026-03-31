# routers/user_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user_schema import UserRegister, UserResponse
from handler.user_handler import create_user, create_tenant_admin
from dependencies.auth import require_admin, get_current_user

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/register", response_model=UserResponse)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    created_user = create_user(db, user, current_user)
    return UserResponse.from_orm(created_user)


@user_router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return UserResponse.from_orm(current_user)


@user_router.post("/register-tenant-admin", response_model=UserResponse)
def register_tenant_admin(
    user: UserRegister,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    created_user = create_tenant_admin(db, user, current_user)
    return UserResponse.from_orm(created_user)