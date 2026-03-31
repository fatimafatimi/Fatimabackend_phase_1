# Project Management API

## Overview

This is a fully-featured **Project Management API** built with **FastAPI**. The project demonstrates a complete, production-ready backend system implementing modern API development concepts including authentication, role-based access control, database migrations, email notifications, and payment processing.

This repository is the **final merged version** incorporating all individual branches and features:

* **FastAPI Day 2, Day 3, Day 4** – Fundamental FastAPI concepts and REST API design.
* **JWT Auth** – User authentication with JWT tokens.
* **Handler Config** – Structured request handling and separation of concerns.
* **Alembic** – Database migrations management.
* **Rollbase** – Base models and reusable project structures.
* **RBAC with Permissions** – Role-based access control with permission management.
* **FastAPI Concepts** – Advanced FastAPI features and dependency injection.
* **Payment Module** – Subscription and payment integration (Stripe).
* **Email Notification** – Email notifications and email verification workflow.

---

## Features

* **User Management**

  * User registration and login
  * JWT-based authentication
  * Role-based access control (Admin / User)
  * Email verification system

* **Project Management**

  * Create, read, update, delete (CRUD) projects
  * Assign users to projects based on permissions
  * Pagination and filtering support

* **Payments**

  * Subscription creation and cancellation
  * Stripe sandbox integration
  * Payment notification emails

* **Notifications**

  * Email notifications for important events
  * Verification emails for new users

* **Database & Migrations**

  * SQLAlchemy ORM
  * Alembic migrations for database schema management

---

## Folder Structure

```
project-management-api/
│
├── app/
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Configuration and environment settings
│   ├── database.py              # Database connection and session management
│   ├── models/                  # SQLAlchemy models
│   │   ├── user.py
│   │   ├── project.py
│   │   └── role_permission.py
│   ├── schemas/                 # Pydantic request/response schemas
│   ├── handlers/                # Business logic handlers
│   ├── routers/                 # API routes grouped by functionality
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── projects.py
│   │   ├── payments.py
│   │   └── webhooks.py
│   ├── dependencies/            # Dependency injection and permissions
│   ├── services/                # External services (Stripe, Email)
│   └── utils/                   # Utility functions
│
├── migrations/                  # Alembic migrations
├── requirements.txt             # Python dependencies
├── README.md
└── .env.example                 # Example environment variables
```

---

## Requirements

* Python 3.11+
* PostgreSQL database
* Stripe Sandbox account for payment testing
* SMTP-enabled email account for notifications

---

## Installation and Setup

1. **Clone the repository**

```bash
git clone https://github.com/fatimafatimi/Fatimabackend_phase_1
cd project-management-api
```

2. **Create a virtual environment**

```bash
python -m venv .venv
```

3. **Activate the virtual environment**

* **Windows (CMD)**:

```bash
.venv\Scripts\activate
```

* **Linux / macOS**:

```bash
source .venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Set up environment variables**

Create a `.env` file based on `.env.example`:

```
DATABASE_URL=postgresql://username:password@localhost:5432/db_name
SECRET_KEY=your_jwt_secret
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
STRIPE_API_KEY=your_stripe_key
```

6. **Run database migrations**

```bash
alembic upgrade head
```

7. **Seed initial roles and permissions (RBAC)**

```bash
python seed_rbac.py
```

---

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

* Interactive API documentation: `http://127.0.0.1:8000/docs`
* Alternative ReDoc documentation: `http://127.0.0.1:8000/redoc`

---

## API Endpoints Overview

**Authentication**

* `POST /auth/register` – Create a new user
* `POST /auth/login` – Login and retrieve JWT token
* `GET /auth/me` – Get current user information (protected)

**Users**

* `GET /users/` – List all users (admin only)
* `GET /users/{id}` – Get user details
* `PATCH /users/{id}` – Update user info
* `DELETE /users/{id}` – Delete user

**Projects**

* `POST /projects/` – Create project
* `GET /projects/` – List projects
* `GET /projects/{id}` – Retrieve a single project
* `PATCH /projects/{id}` – Update project
* `DELETE /projects/{id}` – Delete project

**Payments**

* `POST /subscription/create` – Create subscription
* `POST /subscription/cancel` – Cancel subscription
* `POST /webhook` – Stripe webhook for payment events

**Email Verification**

* `POST /email/verify` – Verify user email
* `POST /email/resend` – Resend verification email

---

## Notes

* Make sure to **run migrations** before starting the application.
* Ensure your SMTP settings are correct to send email notifications.
* Use Stripe **sandbox keys** for testing payments to avoid real transactions.
* RBAC and permissions must be seeded before creating users with specific roles.

---
