#!/usr/bin/env python3
"""
Database initialization and seeding script.

This script creates the database tables and seeds an initial admin user.
Run this script to set up the database for the first time.
"""

import sys
import os

# Add the parent directory to the path so we can import from the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from db.session import engine, SessionLocal, Base
from models.user import User, RoleEnum
from core.security import hash_password


def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


def seed_admin_user():
    """Create an initial admin user."""
    db: Session = SessionLocal()
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(
            User.email == "admin@example.com"
        ).first()
        
        if existing_admin:
            print("⚠️  Admin user already exists!")
            return
        
        # Create admin user
        admin_user = User(
            name="Administrator",
            email="admin@example.com",
            password_hash=hash_password("admin123"),
            role=RoleEnum.admin
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"   Email: admin@example.com")
        print(f"   Password: admin123")
        print(f"   ID: {admin_user.id}")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Main function to initialize database and seed data."""
    print("🚀 Initializing database...")
    
    try:
        create_tables()
        seed_admin_user()
        print("\n🎉 Database initialization completed successfully!")
        print("\nYou can now start the API server with:")
        print("   uvicorn main:app --reload")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()