# WebSockets in Mini Project Management System (Mini PMS)

This document explains the WebSocket implementation in the Mini PMS project built using **FastAPI**, including setup, architecture, and testing guide.

---

# Overview

This project implements a **real-time communication system** using WebSockets inside a Project Management System (PMS).

It enables:

*  Real-time chat between users in the same project
*  Real-time task notifications (create, update, delete)
*  Project-based communication rooms

---

#  Features Implemented

##  1. Real-time Chat

* Users join a project room
* Send and receive messages instantly
* Messages are broadcast to all users in the same project

##  2. Task Notifications

Automatically broadcasts events when:

* Task is created
* Task is updated
* Task is deleted

##  3. Project-based Rooms

* Each project has its own WebSocket room
* Example:

  * `/ws/project/1`
  * `/ws/project/21`

Users only receive updates for their selected project.

---

# Architecture Flow

```
Frontend (Browser)
      ↓ WebSocket connection
FastAPI WebSocket Routes
      ↓
Connection Manager (groups by project_id)
      ↓
Broadcast System
      ↓
All connected clients in same project room
```

---

#  Backend Components

## 1. Connection Manager

Handles active WebSocket connections grouped by project ID.

Responsibilities:

* Connect users
* Disconnect users
* Broadcast messages to project room

---

## 2. WebSocket Routes

Path:

```
/ws/project/{project_id}
```

Responsibilities:

* Accept WebSocket connections
* Receive chat messages
* Broadcast messages to project users

---

## 3. Event System

Located in `websocket/events.py`

Triggers real-time updates for:

* task_created_event
* task_updated_event
* task_deleted_event

---

## 4. Task Handler Integration

Whenever a task operation occurs:

* Database is updated
* WebSocket event is triggered
* Message is broadcast to project users

---

# How to Run the Server

## 1. Activate Virtual Environment

```bash
.venv\Scripts\activate
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Run FastAPI Server

```bash
uvicorn main:app --reload
```

Server will run at:

```
http://127.0.0.1:8000
```

---

# 🧪 How to Test WebSockets

## Step 1: Open Browser Console

* Open Chrome
* Right click → Inspect → Console

---

## Step 2: Connect to WebSocket

### Example (Project 21)

```javascript
let ws = new WebSocket("ws://127.0.0.1:8000/ws/project/21");

ws.onopen = () => console.log("Connected");
ws.onmessage = (event) => console.log("Received:", event.data);
ws.onclose = () => console.log("Disconnected");
```

---

## Step 3: Open Second User (Optional)

```javascript
let ws2 = new WebSocket("ws://127.0.0.1:8000/ws/project/21");

ws2.onmessage = (event) => console.log("User2:", event.data);
```

---

## Step 4: Test Chat

```javascript
ws.send(JSON.stringify({
  user: "Fatima",
  message: "Hello team"
}));
```

### Expected Output:

```json
{
  "type": "chat",
  "user": "Fatima",
  "message": "Hello team"
}
```

---

## Step 5: Test Task Events

Use Swagger or Postman:

### Create Task

```
POST /tasks/21
```

### Example Body:

```json
{
  "title": "New Task",
  "description": "Testing WebSockets",
  "assigned_user_id": 1
}
```

---

## Expected WebSocket Output

```json
{
  "type": "task_created",
  "task_id": 1,
  "title": "New Task",
  "project_id": 21
}
```

---

## Step 6: Test Update Task

```
PUT /tasks/{task_id}
```

### Expected:

```json
{
  "type": "task_updated",
  "task_id": 1,
  "status": "updated",
  "project_id": 21
}
```

---

## Step 7: Test Delete Task

```
DELETE /tasks/{task_id}
```

### Expected:

```json
{
  "type": "task_deleted",
  "task_id": 1,
  "project_id": 21
}
```

