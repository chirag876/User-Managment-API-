"""
Pydantic schemas for user-related data validation and serialization.

This module defines Pydantic models for handling user data in API requests and
responses. `UserCreate` is used for validating input data when creating a new user,
ensuring a valid name, email, and password. `UserLogin` validates login credentials
with email and password. `UserOut` defines the response structure for user data,
including a UUID identifier, name, email, and role, with ORM mode enabled for
compatibility with SQLAlchemy models.
"""
import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict   # 👈 yeh import missing tha

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)  
