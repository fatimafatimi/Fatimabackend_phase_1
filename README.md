# 🚀 Day 02 – Structured Task API
### 📌 Project Overview

Day 02 upgrades the Day 01 Task API into a clean, modular, and scalable backend structure.

The application was refactored using APIRouter, separate schema models, proper validation rules, and REST-compliant status codes.

### 🎯 Objective

The goal of Day 02 was to:

Refactor the API into a professional structure

Implement request and response models separately

Add input validation

Use correct HTTP status codes

Improve code organization

### 📂 Project Structure
project/
│

├── main.py

├── config.py
│

├── routers/

│   └── tasks.py
│

├── models/

│   └── task.py
│

└── schemas/

  └── task_schema.py
    

### 🛠️ Improvements Over Day 01

Routes moved to APIRouter

Separation of concerns implemented

Added TaskCreate and TaskResponse models

Title validation (minimum 3 characters)

Proper REST status codes (201, 204, 404, 422)

Response model enforcement

### 📌 Endpoints
Method	Endpoint	Description
GET	/	Welcome message
GET	/tasks	Retrieve all tasks
POST	/tasks	Create task (validated)
GET	/tasks/{task_id}	Retrieve specific task
DELETE	/tasks/{task_id}	Delete specific task

### 🔎 Validation Example

If title has fewer than 3 characters:

422 Unprocessable Entity


FastAPI automatically handles validation errors using Pydantic.

### ▶️ How to Run

Activate virtual environment

Install dependencies:

pip install fastapi uvicorn


Run server:

uvicorn main:app --reload


Visit:

http://127.0.0.1:8000/docs

### 🧠 Concepts Learned

Modular FastAPI architecture

APIRouter usage

Request & response model separation

Response validation

RESTful status codes

Scalable backend structure

### 🚀 Learning Outcome

Day 02 transformed the basic CRUD API into a structured, production-style backend application following clean architecture principles.
