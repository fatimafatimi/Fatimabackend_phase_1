# Mini PMS — Multi-Tenant Project Management API

A multi-tenant REST API built with FastAPI and PostgreSQL for managing projects, tasks, roles, and permissions across isolated tenants. Supports a three-tier user hierarchy: Super Admin, Tenant Admin, and regular Users. Authentication is handled via JWT tokens with OTP-based email verification and a full forgot password flow.

---

## Tech Stack

- **Python** 3.13
- **FastAPI** — web framework
- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **Pydantic v2** — data validation
- **JWT (python-jose)** — authentication tokens
- **Passlib + bcrypt** — password hashing
- **dnspython** — real-world email existence verification
- **uv** — package manager

---

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│                  Super Admin                │
│         (global access, all tenants)        │
└──────────────────┬──────────────────────────┘
                   │ registers
     ┌─────────────▼─────────────┐
     │       Tenant Admin        │
     │  (scoped to own tenant)   │
     └─────────────┬─────────────┘
                   │ creates
          ┌────────▼────────┐
          │   Tenant User   │
          │ (own resources) │
          └─────────────────┘
```

Each tenant is fully isolated. A Tenant Admin and their users cannot see or modify data belonging to another tenant.

---

## User Roles

### Super Admin
- Single global administrator, not scoped to any tenant
- Can register new Tenant Admins (which also creates a new tenant automatically)
- Has unrestricted access to all projects, tasks, roles, and permissions across all tenants
- Bypasses all permission checks globally

### Tenant Admin
- Scoped entirely to their own tenant
- Has full admin capabilities within their tenant — projects, tasks, roles, permissions
- Can create users within their tenant
- Cannot access or modify another tenant's data

### User (Normal / Tenant)
- Can create, update, view, and delete their own projects
- Can create, update, view, and delete tasks within their own projects
- Cannot access roles or permissions
- Cannot access another tenant's data (if a tenant user)

---

## Project Structure

```
Mini PMS/
├── main.py
├── database.py
├── config/
│   └── config.py
├── models/
│   ├── user.py
│   ├── tenant.py
│   ├── project.py
│   ├── task.py
│   ├── role.py
│   └── permission.py
├── schemas/
│   ├── user_schema.py
│   ├── project_schema.py
│   ├── task_schema.py
│   ├── role.py
│   └── permission.py
├── routers/
│   ├── auth_router.py
│   ├── user_routes.py
│   ├── project_router.py
│   ├── task_router.py
│   ├── role_router.py
│   └── permission_router.py
├── handler/
│   ├── user_handler.py
│   ├── project_handler.py
│   ├── task_handler.py
│   ├── role_handler.py
│   └── permission_handler.py
├── dependencies/
│   ├── auth.py
│   └── permissions.py
├── utils/
│   ├── security.py
│   ├── jwt_handler.py
│   ├── otp_utils.py
│   └── email_service.py
├── alembic/
│   ├── env.py
│   └── versions/
├── alembic.ini
└── scripts/
    └── migrate_existing_users.py
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/fatimafatimi/Fatimabackend_phase_1
cd "Mini PMS"
```

### 2. Create and activate virtual environment

```bash
uv venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux
```

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 4. Set up PostgreSQL

Create a database:

```sql
CREATE DATABASE mini_pms;
```

### 5. Configure environment variables

Create a `.env` file in the root directory (see [Environment Variables](#environment-variables)).

### 6. Run Alembic migrations

```bash
alembic upgrade head
```

### 7. Seed the database

```bash
python -m scripts.migrate_existing_users
```

This script:
- Creates a Default tenant if none exists
- Seeds all permissions and roles for every existing tenant
- Migrates any users without a tenant to the Default tenant
- Fixes any roles that have no permissions assigned

---

## Environment Variables

Create a `.env` file in the root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/mini_pms
SECRET_KEY=your_secret_key_here
```

---

## Running the App

```bash
uv run uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

Interactive Swagger docs: `http://127.0.0.1:8000/docs`

---

## Authentication Flow

All protected endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

### Login

```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=yourpassword
```

Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "tenant_id": 1
}
```

## Multi-Tenant Isolation

### How it works

Every major resource — `User`, `Project`, `Task`, `Role`, `Permission` — has a `tenant_id` foreign key. All queries for non-super-admin users are automatically filtered by `tenant_id` at the handler level.

### Tenant creation flow

```
Super Admin calls POST /users/register-tenant-admin
    → New Tenant record is created
    → admin and user roles are created for that tenant
    → All 12 permissions are seeded for that tenant
    → Correct permissions are assigned to each role
    → Tenant Admin user is created with the admin role
```

### Data isolation rules

- A Tenant Admin can only see and modify resources where `tenant_id` matches their own
- A regular user can only modify resources they own (`owner_id == user.id`) within their tenant
- The Super Admin bypasses all tenant checks and sees everything globally

### Previous users (pre-multi-tenant)

Users created before multi-tenant was implemented are assigned to the **Default** tenant via the migration script. They behave exactly like regular users scoped to that tenant.

---

## Notes

- Tokens expire after **30 minutes** by default. Re-login to get a fresh token.
- When testing in Swagger, do not send `assigned_user_id: 0` in task requests — either omit the field or set it to `null`. The value `0` is not a valid user ID.
- The Super Admin account must be created directly in the database or via a separate seeding script — there is no public registration endpoint for Super Admins by design.
