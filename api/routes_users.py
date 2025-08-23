"""
This module defines user-related API routes for the User Management system.

Key Responsibilities:
- Register new users (with unique email validation and hashed password storage).
- Provide a "Get My Profile" endpoint for logged-in users.
- Fetch user details by ID (RBAC: only self or admin can access).
- List all users with pagination (admin-only access).

Dependencies:
- FastAPI's APIRouter and dependency injection.
- SQLAlchemy ORM session for database interaction.
- JWT decoding for authentication.
- User service functions for business logic.
- Role-based access control using RoleEnum.
"""

from typing import List

from core.security import decode_token
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.user import RoleEnum, User
from schemas.user import UserCreate, UserOut
from services import user_service
from sqlalchemy.orm import Session

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.post("", response_model=UserOut, status_code=201)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if user_service.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    return user_service.create_user(db, user_in)


@router.get("/userprofile", response_model=UserOut)
def get_userprofile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{id}", response_model=UserOut)
def get_user(id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if str(current_user.id) != id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("", response_model=List[UserOut])
def list_users(page: int = 1, limit: int = 20, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Admins only")
    limit = min(limit, 100)
    offset = (page - 1) * limit
    users = db.query(User).offset(offset).limit(limit).all()
    return users
