"""
User CRUD operations for managing user data in the database.

This module provides functions for creating and retrieving users from the database
using SQLAlchemy. The `create_user` function creates a new user by hashing the
provided password and storing the user data, then committing it to the database.
The `get_user_by_email` function retrieves a user by their email address, returning
the first matching record or None if no user is found.
"""
from sqlalchemy.orm import Session

from core.security import hash_password
from models.user import User
from schemas.user import UserCreate


def create_user(db: Session, user_in: UserCreate):
    user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
