"""
Security utilities for password hashing and JWT-based authentication.

This module provides functions for securely hashing passwords, verifying passwords,
creating JWT access tokens, and decoding JWT tokens. It integrates with the FastAPI
application's configuration settings (from `core.config`) to manage token expiration
and secret keys. The module uses `passlib` for password hashing with bcrypt and
`python-jose` for JWT encoding and decoding.

Key Components:
- `pwd_context`: A `CryptContext` instance configured to use bcrypt for password
  hashing, with automatic handling of deprecated schemes.
- `hash_password`: Hashes a plain-text password using bcrypt.
- `verify_password`: Verifies a plain-text password against a hashed password.
- `create_access_token`: Generates a JWT access token with a configurable expiration
  time, signed with the `JWT_SECRET` from settings.
- `decode_token`: Decodes and validates a JWT token, returning its payload or None if
  invalid.

Dependencies:
- `passlib[bcrypt]`: For password hashing and verification.
- `python-jose[cryptography]`: For JWT encoding and decoding.
- `core.config.settings`: Provides `JWT_SECRET` and `ACCESS_TOKEN_EXPIRES_MIN` for
  token configuration.

Usage:
    ```python
    from core.security import hash_password, create_access_token, decode_token

    # Hash a password
    hashed = hash_password("mypassword")
    
    # Verify a password
    is_valid = verify_password("mypassword", hashed)
    
    # Create a JWT token
    token = create_access_token({"sub": "user_id"})
    
    # Decode a JWT token
    payload = decode_token(token)
    ```

Security Notes:
- The `JWT_SECRET` must be a secure, random string in production (set via `.env`).
- The `ACCESS_TOKEN_EXPIRES_MIN` setting controls token expiration (default: 30 minutes).
- Ensure tokens are transmitted securely (e.g., over HTTPS).
- Handle `None` returns from `decode_token` appropriately in authentication flows.
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MIN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")


def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return payload
    except JWTError:
        return None
