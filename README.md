# Mini Project Management System (Branch: RBAC Implementation)

This branch implements authentication and role-based access control (RBAC) using FastAPI, JWT, and SQLAlchemy.

---

## 🚀 Features Implemented

* User authentication with JWT
* Password hashing using bcrypt
* Role-based access control (Admin & Owner-based permissions)
* Project-task relationship management
* Protected routes using dependencies
* Proper HTTP status handling (401, 403, 404)

---

## 🛠 Tech Stack

* FastAPI
* SQLAlchemy ORM
* JWT Authentication
* OAuth2PasswordBearer
* Passlib (bcrypt)
* SQLite / Configured Database

---

## 🔐 Authentication System

Authentication is handled using JWT tokens.

### Login Flow

1. User logs in using email and password.
2. Password is verified using `verify_password`.
3. If valid, a JWT token is generated containing:

```json
{
  "sub": "user_email",
  "role": "user_role"
}
```

4. Token is returned as:

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

---

## Password Security

Passwords are securely hashed using:

* bcrypt via Passlib

Functions used:

* `hash_password(password)`
* `verify_password(plain_password, hashed_password)`

---

## 👤 User Management

### Create User

* Only users with **admin role** can create new users.
* Implemented using `require_admin` dependency.
* Prevents duplicate email registration.

If email already exists:

* Returns `400 Bad Request`

---

## 📂 Task Management Authorization

Authorization is enforced inside handler logic using:

* Role checking
* Project ownership validation

---

### Create Task

Allowed if:

* User role is `"admin"`
  OR
* User is the owner of the project

Otherwise:

* Returns `403 Forbidden`

---

### Get Tasks by Project

Allowed if:

* User role is `"admin"`
  OR
* User owns the project

---

### Update Task

Allowed if:

* User role is `"admin"`
  OR
* User owns the associated project

Partial updates supported using:

```python
task.dict(exclude_unset=True)
```

---

### Delete Task

Allowed if:

* User role is `"admin"`
  OR
* User owns the associated project

Returns:

```json
{
  "message": "Task deleted"
}
```

---

## 🔐 Authorization Logic Pattern

This branch implements:

### 1️⃣ Role-Based Check

```python
if current_user.role != "admin":
```

### 2️⃣ Ownership Check

```python
project.owner_id == current_user.id
```

This ensures:

* Admin has full access.
* Non-admin users can only manage their own project resources.

---

## 🧱 Security Architecture

Authentication:

* OAuth2PasswordBearer
* JWT token decoding
* get_current_user dependency

Authorization:

* Admin-only access for user creation
* Project ownership validation for task actions
* HTTP 403 for unauthorized access
* HTTP 401 for invalid tokens
* HTTP 404 for missing resources

---

## 📁 Project Structure (Relevant Parts)

```
models/
    user.py
    project.py
    task.py

handlers/
    user_handler.py
    task_handler.py

dependencies/
    auth.py

utils/
    jwt_handler.py
    security.py
```

---

## ✅ What This Branch Demonstrates

* Secure JWT authentication
* Role-based access control (RBAC)
* Ownership-based authorization
* Clean dependency injection in FastAPI
* Proper separation of concerns (models, handlers, dependencies, utils)

---

## 📌 Notes

This branch focuses on:

* Authentication
* Admin-restricted user creation
* Task-level authorization
* Project ownership enforcement

Permission-based dynamic RBAC is not implemented in this branch.


 
