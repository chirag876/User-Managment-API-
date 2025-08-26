"""
This module defines authentication-related API routes for the User Management system.
It handles user login and issues JWT access tokens.

Key Responsibilities:
- Expose /auth/login endpoint for user authentication.
- Validate user credentials against stored records.
- Return a signed JWT token if authentication is successful.
- Deny access with 401 Unauthorized if credentials are invalid.

Dependencies:
- FastAPI's APIRouter for defining routes.
- SQLAlchemy Session for database access.
- OAuth2PasswordBearer and OAuth2PasswordRequestForm for OAuth2 login flow.
- Security utilities (password verification, token creation).
"""

from core.security import create_access_token, verify_password
from core.config import settings
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from services import user_service
from sqlalchemy.orm import Session

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_service.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {
        "access_token": token, 
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRES_MIN * 60  # Convert to seconds
    }
