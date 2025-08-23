"""
User model definition for SQLAlchemy ORM (SQLite Friendly).
This version stores UUID as string for SQLite compatibility.
"""

import enum
import uuid
from sqlalchemy import Column, DateTime, Enum, String, func
from db.session import Base


class RoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    # Store UUID as string because SQLite does not support native UUID
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
