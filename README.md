# 🚀 Day 01 – Simple Task API
### 📌 Project Overview

This project is a basic REST API built using FastAPI.
It demonstrates core backend development concepts including routing, request handling, JSON responses, and automatic documentation.

The API uses in-memory storage (Python list) to manage tasks and performs basic CRUD operations.

### 🎯 Objective

The goal of Day 01 was to:

Understand FastAPI fundamentals

Learn API routing

Work with request bodies

Implement CRUD operations

Explore automatic Swagger documentation

### 🛠️ Tech Stack
Python
FastAPI
Uvicorn

### 📂 Features Implemented
Endpoints

Method	Endpoint	Description

GET	/	Welcome message

GET	/tasks	Retrieve all tasks

POST	/tasks	Create a new task

GET	/tasks/{task_id}	Retrieve task by ID

DELETE	/tasks/{task_id}	Delete task by ID

### 📌 Key Concepts Learned
API Routing with FastAPI

JSON request & response handling

Path parameters

Basic error handling using HTTPException

Pydantic model usage

Swagger UI testing (/docs)

### ▶️ How to Run
Create virtual environment

Install dependencies:

pip install fastapi uvicorn

Run server:

uvicorn main:app --reload

Open:

http://127.0.0.1:8000/docs

### ⚠️ Note
This project uses in-memory storage.

All tasks are lost when the server restarts.

### 🧠 Learning Outcome
By completing Day 01, I gained hands-on experience with building a basic REST API and understanding FastAPI fundamentals.
