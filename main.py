"""
Main application setup for the User Management API using FastAPI.

This module initializes the FastAPI application, sets up the database by creating
all defined tables, and includes routers for authentication and user management
endpoints. The `Base.metadata.create_all` call ensures that the database schema is
created based on the defined SQLAlchemy models. The application includes two routers:
`routes_auth` for authentication-related endpoints and `routes_users` for user-related
endpoints, each with their respective prefixes and tags for API organization.
"""
from fastapi import FastAPI

from api import routes_auth, routes_users
from db.session import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Management API")

# Routers
app.include_router(routes_auth.router, prefix="/auth", tags=["auth"])
app.include_router(routes_users.router, prefix="/users", tags=["users"])
