# Mini PMS — Role-Based Access Control (RBAC) with Permissions

## Overview

This project extends the **Mini Project Management System (PMS)** with a **robust Role-Based Access Control (RBAC) system** using permissions. It allows fine-grained control over what actions each user can perform based on their role and assigned permissions.

Key features:

* Create and manage **Roles**.
* Create and manage **Permissions**.
* Assign multiple **Permissions** to a Role.
* Enforce access control using **permission checks** in API endpoints.
* JWT-based authentication integrated with RBAC.
* PostgreSQL database with SQLAlchemy ORM for reliable data integrity.

---

## Features

### Roles

* Roles represent a group of users with common access rights.
* Roles can have multiple permissions assigned.
* Examples: `admin`, `manager`, `user`.

### Permissions

* Permissions define specific actions a user can perform.
* Examples: `create_project`, `update_project`, `delete_project`, `view_all_projects`.
* Permissions are assigned to roles, not individual users directly.

### RBAC Enforcement

* Endpoints are protected using a **`require_permission`** dependency.
* Example: Only users with `manage_roles` permission can create or assign roles.
* JWT tokens carry user role information.

---

## Database Structure

### Tables

* **users** – Stores user information, including assigned role.
* **roles** – Stores role names.
* **permissions** – Stores permission names.
* **role_permission** – Association table linking roles and permissions (many-to-many).

### Relationships

```
User --(many-to-one)--> Role --(many-to-many)--> Permission
```

* A **User** belongs to one Role.
* A **Role** can have multiple Permissions.
* A **Permission** can be assigned to multiple Roles.

---

## API Endpoints

### Role Endpoints

| Method | Endpoint                       | Description                       | Permission Required |
| ------ | ------------------------------ | --------------------------------- | ------------------- |
| POST   | `/roles/`                      | Create a new role                 | `manage_roles`      |
| GET    | `/roles/{role_id}`             | Get role details with permissions | `manage_roles`      |
| POST   | `/roles/{role_id}/permissions` | Assign permissions to a role      | `manage_roles`      |
| GET    | `/roles/`                      | List all roles with permissions   | `manage_roles`      |

### Permission Endpoints

| Method | Endpoint        | Description             | Permission Required  |
| ------ | --------------- | ----------------------- | -------------------- |
| POST   | `/permissions/` | Create a new permission | `manage_permissions` |
| GET    | `/permissions/` | List all permissions    | `manage_permissions` |

---

## Example Usage (Swagger / Postman)

### 1. Create a Role

```json
POST /roles/
{
    "name": "manager"
}
```

### 2. Create a Permission

```json
POST /permissions/
{
    "name": "create_project"
}
```

### 3. Assign Permissions to a Role

```json
POST /roles/1/permissions
{
    "permission_names": ["create_project", "update_project", "view_all_projects"]
}
```

### 4. Get Role with Permissions

```json
GET /roles/1
```

**Response:**

```json
{
    "id": 1,
    "name": "manager",
    "permissions": ["create_project", "update_project", "view_all_projects"]
}
```

---

## Technologies Used

* **FastAPI** – Modern Python web framework.
* **SQLAlchemy** – ORM for database interactions.
* **PostgreSQL** – Relational database with strong data integrity.
* **Pydantic** – Data validation and serialization.
* **JWT** – JSON Web Tokens for authentication.
* **Swagger UI** – Automatic API documentation and testing.

---

## How It Works

1. **Users** are assigned a **Role**.
2. **Roles** have one or more **Permissions**.
3. API endpoints check user permissions using the `require_permission` dependency.
4. Unauthorized access attempts return a `403 Forbidden` error.
5. Admins can manage roles and permissions dynamically without changing code.

---

## Setup Instructions

1. Clone the repository:

```bash
git clone <repo-url>
cd Mini-PMS
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure the PostgreSQL database in `database.py`.

5. Run migrations (Alembic recommended):

```bash
alembic upgrade head
```

6. Start the server:

```bash
uvicorn main:app --reload
```

7. Access Swagger UI at:

```
http://127.0.0.1:8000/docs
```

---

## Benefits of This RBAC System

* **Flexible access control** – Assign permissions at the role level.
* **Secure** – Users can only access actions allowed by their role.
* **Scalable** – Easily add new roles and permissions without changing code.
* **Traceable** – Easy to see which role has what permissions.

---

