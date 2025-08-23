import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db.session import Base, get_db
from core.security import hash_password
from models.user import User, RoleEnum

# --- Setup test database ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)

# --- Helpers ---
def create_admin(db):
    admin = User(
        name="Admin",
        email="admin@example.com",
        password_hash=hash_password("admin123"),
        role=RoleEnum.admin,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    create_admin(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

# --- Tests ---
def test_register_user():
    res = client.post("/users", json={"name": "John", "email": "john@example.com", "password": "pass123"})
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "john@example.com"
    assert "id" in data

def test_login_user():
    res = client.post("/auth/login", data={"username": "john@example.com", "password": "pass123"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    global user_token
    user_token = data["access_token"]

def test_get_me():
    headers = {"Authorization": f"Bearer {user_token}"}
    res = client.get("/users/me", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "john@example.com"

def test_user_cannot_access_other_user():
    headers = {"Authorization": f"Bearer {user_token}"}
    # Admin id is in db
    db = TestingSessionLocal()
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    db.close()
    res = client.get(f"/users/{admin.id}", headers=headers)
    assert res.status_code == 403

def test_admin_can_list_users():
    # login admin
    res = client.post("/auth/login", data={"username": "admin@example.com", "password": "admin123"})
    assert res.status_code == 200
    admin_token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {admin_token}"}

    res = client.get("/users", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1
