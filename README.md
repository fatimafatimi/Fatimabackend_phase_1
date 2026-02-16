# Mini Project Management System (Day 04)  
**Technology:** FastAPI + PostgreSQL + SQLAlchemy  

## Overview
This project is a **backend system** to manage Users, Projects, and Tasks.  
It allows users to register, login, create projects, assign tasks, and track task status (`pending`, `in_progress`, `completed`) using a PostgreSQL database.

---

## Features
- **User Management:** Register and login users.  
- **Project Management:** Create, view all, and view specific projects.  
- **Task Management:** Create tasks under a project, retrieve tasks by ID or project.  
- **Database:** Persistent storage using PostgreSQL and SQLAlchemy ORM.  
- **API Documentation:** Interactive testing via Swagger UI (`/docs`).  

---

## Project Structure
```

Project/
├── main.py              # App entry point
├── database.py          # Database connection & session
├── models/              # ORM models (User, Project, Task)
├── schemas/             # Pydantic request/response models
├── routers/             # API routes (users, projects, tasks)
└── .env                 # Database credentials

````

---

## Getting Started

1. **Clone the repository**  
```bash
git clone <repo-url>
cd Mini-PMS
````

2. **Set up virtual environment & install dependencies**

```bash
python -m venv menv
source menv/Scripts/activate  # Windows
pip install -r requirements.txt
```

3. **Configure `.env` file**

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/taskdb
```

4. **Run the server**

```bash
uvicorn main:app --reload
```

5. **Test API via Swagger UI**
   Open: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Endpoints Overview

* **Users:** `/users/registers`, `/users/login`
* **Projects:** `/projects/` (POST, GET, GET by ID)
* **Tasks:** `/tasks/project/{project_id}/tasks`, `/tasks/`

---

## Key Learnings

* Modular backend design with **APIRouter**
* SQLAlchemy ORM and database relationships
* Dependency injection for database sessions
* Persistent storage and relational data integrity
* Testing API endpoints using **Swagger UI**

