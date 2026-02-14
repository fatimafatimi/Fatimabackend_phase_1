# 📌 Day 03 – Task API with Database (FastAPI + PostgreSQL)

### 🚀 Overview

This project implements a **Task Management API** using:

* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic

---

### 🎯 Objectives Completed

✅ Connect FastAPI to PostgreSQL

✅ Create Task table using SQLAlchemy ORM

✅ Implement CRUD operations

✅ Store tasks in database (persistent storage)

✅ Use Dependency Injection for DB session handling

✅ Proper project structure and layering

---

### 📂 Project Structure

```
project/

 main.py
 config.py
 db.py

 routers/
   tasks.py

 models/
   task.py

 schemas/
   task_schema.py
```

---

### 🗄️ Database Setup

Make sure PostgreSQL is installed and running.

Create a database:

```sql
CREATE DATABASE taskdb;
```

Update your `config.py` with your database credentials:

```python
DATABASE_URL = "postgresql://username:password@localhost/taskdb"
```

---

## ⚙️ How to Run the Project

### 1️⃣ Activate Virtual Environment

```bash
venv\Scripts\activate
```

### 2️⃣ Install Dependencies (if not installed)

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary
```

### 3️⃣ Run the Server

```bash
uvicorn main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

# 📌 API Endpoints

#### ➕ Create Task

`POST /tasks`

```json
{
  "title": "Learn FastAPI",
  "description": "Practice CRUD"
}
```

---

#### 📄 Get All Tasks

`GET /tasks`

---

#### ✏️ Update Task

`PUT /tasks/{id}`

---

#### ❌ Delete Task

`DELETE /tasks/{id}`

---

## 🧠 Key Concepts Implemented

### 1️⃣ ORM (Object Relational Mapping)

Using SQLAlchemy ORM to map Python classes to database tables.

---

### 2️⃣ Dependency Injection

Database session is injected into routes using FastAPI's `Depends()`.

This ensures:

* Clean session handling
* Automatic DB connection closing
* Scalable architecture

---

### 3️⃣ Pydantic Schemas

Used for:

* Request validation
* Response serialization
* ORM object conversion using:

```python
model_config = {
    "from_attributes": True
}
```

---

### 4️⃣ Database Persistence

Data is stored in PostgreSQL, not in memory.

To verify persistence:

* Insert a task
* Restart server
* Data still exists → ✅ confirmed

---

### 🔍 Testing

You can test the API using:

* Swagger UI
  `http://127.0.0.1:8000/docs`

* Or pgAdmin to check database rows directly

