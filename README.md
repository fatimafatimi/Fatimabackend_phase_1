# JWT Authentication – Mini Project Management System
## 📌 Overview

This branch implements **JWT (JSON Web Token) Authentication** for the Mini Project Management System built with:

* FastAPI
* PostgreSQL
* SQLAlchemy
* Passlib (bcrypt)
* Python-JOSE (JWT)

The authentication system secures user login and protects API routes using access tokens.

---

## 🚀 Features Implemented

* User Registration with password hashing
* User Login with password verification
* JWT Access Token generation
* Token expiration handling
* Protected routes using dependency injection
* Manual Authorization header validation
* Swagger UI authentication removed (manual header usage)

---

## 🏗 Project Structure

```
Project/
├── main.py
├── database.py
├── routers/
│   └── user_routes.py
    └── task_routes.py
    └── project_routes.py
    └── __init__.py
├── models/
│   └── user.py
    └── project.py
    └── task.py
    └── __init__.py
├── schemas/
│   └── user_schema.py
    └── task_schema.py
    └── project_schema.py
    └── __init__.py
├── utils/
│   ├── jwt_handler.py
    └── security.py
    └── dependencies.py
└── .env
```

---

## 🔐 JWT Authentication Flow

1. User registers → password is hashed and stored.
2. User logs in → password is verified.
3. Server generates JWT token.
4. Client sends token in request header.
5. Protected routes validate token before returning data.

---

## ⚙️ Installation & Setup

### 1️⃣ Create Virtual Environment

```bash
python -m venv menv
```

Activate environment:

Windows:

```bash
menv\Scripts\activate
```

Mac/Linux:

```bash
source menv/bin/activate
```

---

### 2️⃣ Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-dotenv
```

---

### 3️⃣ Configure Database

Create PostgreSQL database:

```
taskdb
```

Update `.env` file:

```
DATABASE_URL=postgresql://username:password@localhost/taskdb
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 4️⃣ Run the Server

```bash
uvicorn main:app --reload
```

Open browser:

```
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

### 🔹 Register User

```
POST /users/register
```

Request Body:

```json
{
  "username": "fatima",
  "email": "fatima@example.com",
  "password": "mypassword123"
}
```

---

### 🔹 Login User

```
POST /users/login
```

Response:

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

---

### 🔹 Get Current User (Protected Route)

```
GET /users/me
```

Header:

```
Authorization: Bearer <JWT_TOKEN>
```

---

## 🧪 Testing with cURL

### Login

```bash
curl -X POST "http://127.0.0.1:8000/users/login" -H "Content-Type: application/json" -d "{\"email\":\"fatima@example.com\",\"password\":\"mypassword123\"}"
```

### Access Protected Route

```bash
curl -X GET "http://127.0.0.1:8000/users/me" -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🔐 Security Concepts Used

* JWT Token Structure (Header + Payload + Signature)
* Secret Key Encryption
* Token Expiration
* Bearer Token Authentication
* Password Hashing using bcrypt
* Dependency Injection for route protection
* HTTP 401 Unauthorized handling

---

## ❗ Common Errors

### 401 Unauthorized

* Token missing
* Token expired
* Invalid token

### 400 Bad Request

* Incorrect login credentials

### 404 Not Found

* User does not exist

---

# 📚 Concepts Learned

* Implementing JWT authentication from scratch
* Secure password hashing
* Protecting routes in FastAPI
* Manual header parsing
* Modular backend architecture
* Secure API design practices

---

