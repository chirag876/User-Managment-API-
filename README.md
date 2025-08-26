# User Management API
A production-ready User Management REST API built with secure practices and clean architecture. Supports user registration, JWT-based authentication, profile retrieval, and paginated user listing. Emphasizes clarity, maintainability, and code quality for real-world use.

---

## 🎯 Features
- Register new users (passwords hashed with bcrypt)
- JWT-based authentication (login)
- Get logged-in user's profile (`/me`)
- Fetch user by ID (self or admin access)
- Paginated user listing (admin only)
- Environment-based configuration
- Auto-generated API docs with Swagger/OpenAPI

---

## ⚙️ Setup

### Requirements
- Python **3.10+**
- Virtual environment recommended

### Steps
```bash
# Clone repo
git clone <your-repo-url>
cd User-Managment-API-

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional)
cp .env.example .env
# Edit .env with your preferred settings

# Initialize database and create admin user
python db/seed.py

# Start the server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Environment Variables
The following environment variables can be configured in a `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection URL | `sqlite:///./user.db` |
| `JWT_SECRET` | Secret key for JWT tokens | `supersecret_change_this_in_production` |
| `ACCESS_TOKEN_EXPIRES_MIN` | Token expiration time in minutes | `30` |

⚠️ **Important**: Change `JWT_SECRET` to a secure random string in production!

---

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔗 API Endpoints

### Authentication
- `POST /auth/login` - User login (returns JWT token)

### Users
- `POST /users` - Register new user
- `GET /users/me` - Get current user profile (requires auth)
- `GET /users/{id}` - Get user by ID (requires auth, RBAC)
- `GET /users` - List all users with pagination (admin only)

### Example Requests

#### Register User
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "password": "securepass123"}'
```

#### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=securepass123"
```

#### Get Profile
```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### List Users (Admin Only)
```bash
curl -X GET "http://localhost:8000/users?page=1&limit=10" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN"
```

---

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage (optional)
pip install pytest-cov
python -m pytest tests/ --cov=. --cov-report=html
```

### Default Admin Account
The database seed script creates a default admin account:
- **Email**: `admin@example.com`
- **Password**: `admin123`

Use this account to test admin-only endpoints.

---

## 🏗️ Project Structure

```
├── api/                    # API route handlers
│   ├── routes_auth.py     # Authentication endpoints
│   └── routes_users.py    # User management endpoints
├── core/                  # Core application logic
│   ├── config.py         # Configuration settings
│   └── security.py       # Security utilities (JWT, hashing)
├── db/                    # Database layer
│   ├── session.py        # Database session management
│   └── seed.py           # Database initialization script
├── models/                # SQLAlchemy ORM models
│   └── user.py           # User model
├── schemas/               # Pydantic schemas
│   └── user.py           # User validation schemas
├── services/              # Business logic layer
│   └── user_service.py   # User CRUD operations
├── tests/                 # Test suite
│   └── test_users.py     # User endpoint tests
├── main.py               # FastAPI application entry point
├── requirements.txt      # Python dependencies
└── .env.example         # Environment variables template
```

---

## 🔐 Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Authentication**: Stateless authentication with configurable expiration
- **Role-Based Access Control**: User and Admin roles with proper permissions
- **Input Validation**: Comprehensive request/response validation with Pydantic
- **SQL Injection Protection**: Uses SQLAlchemy ORM with parameterized queries

---

## 📝 Development Notes

### Time Spent: ~4-5 hours
### Trade-offs Made:
- Used SQLite for simplicity (easily switchable to PostgreSQL)
- UUID stored as string for SQLite compatibility
- Basic pagination without cursor-based optimization
- Simple RBAC (could be extended with more granular permissions)

---

## 🚀 Production Deployment

For production deployment:

1. **Use PostgreSQL** instead of SQLite
2. **Set secure environment variables**:
   ```bash
   export JWT_SECRET="your-super-secure-random-string-here"
   export DATABASE_URL="postgresql://user:pass@localhost/dbname"
   ```
3. **Use a proper WSGI server** like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   ```
4. **Set up reverse proxy** (nginx, Apache)
5. **Enable HTTPS** for secure token transmission
6. **Consider rate limiting** for login endpoints
7. **Set up monitoring and logging**
