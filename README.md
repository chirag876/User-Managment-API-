# User-Managment-API
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
cd user-management-api

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
