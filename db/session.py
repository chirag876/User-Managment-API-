"""
Database configuration and session management for SQLAlchemy.

This module sets up the SQLAlchemy engine, session factory, and base class for
ORM models. It uses the DATABASE_URL from the settings configuration to create
a database engine with specific connection arguments to handle SQLite threading.
The `SessionLocal` is a session factory for creating database sessions. The
`get_db` function is a generator that provides a database session and ensures it
is properly closed after use, suitable for dependency injection in FastAPI or
similar frameworks.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={
                       "check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
