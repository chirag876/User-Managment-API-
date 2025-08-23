"""
Configuration management for the FastAPI application using Pydantic's BaseSettings.

This module defines a `Settings` class that centralizes application configuration,
including database connection details and JWT authentication settings. It leverages
Pydantic's `BaseSettings` to provide type-safe configuration with automatic environment
variable parsing and support for loading values from a `.env` file.

Attributes:
    DATABASE_URL (str): The database connection URL (defaults to SQLite database at
        './user.db'). Can be overridden via the `DATABASE_URL` environment variable.
    JWT_SECRET (str): The secret key used for signing and verifying JWT tokens
        (defaults to 'supersecret'). Should be overridden with a secure value in
        production via the `JWT_SECRET` environment variable.
    ACCESS_TOKEN_EXPIRES_MIN (int): The expiration time for JWT access tokens in
        minutes (defaults to 30). Can be overridden via the
        `ACCESS_TOKEN_EXPIRES_MIN` environment variable.

The `Settings.Config` inner class specifies that environment variables can be loaded
from a `.env` file, allowing for flexible configuration in different environments
(e.g., development, production).

Usage:
    The `settings` instance can be imported and used across the application to access
    configuration values, such as in database initialization or JWT token generation.

Example:
    ```python
    from config import settings
    print(settings.DATABASE_URL)  # Outputs: sqlite:///./user.db or value from .env
    ```

Note:
    - Ensure the `.env` file is present in the project root if environment variable
      overrides are needed.
    - For production, set a secure `JWT_SECRET` and use a robust database URL
      (e.g., PostgreSQL or MySQL) instead of SQLite.
    - The SQLite database file (`user.db`) will be created in the project root if it
      does not already exist.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./user.db"
    JWT_SECRET: str = "supersecret"
    ACCESS_TOKEN_EXPIRES_MIN: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
