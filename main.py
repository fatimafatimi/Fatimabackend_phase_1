from fastapi import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel

#GET / → Welcome message
app= FastAPI()

tasks=[]

@app.get("/")
def welcome():
    return {"message": "Welcome" }
    

#GET /tasks → Return list of tasks
@app.get("/tasks")
def list_of_tasks():
    return tasks


#POST /tasks → Add a task
class Task(BaseModel):
    title: str
    description: str

@app.post("/tasks")
def add_task(task: Task):
    global current_id
    task_dict=task.dict()
    task_dict["id"]=current_id
    tasks.append(task_dict)
    current_id += 1
    return {"message": "Task Added" , "task": task_dict}

#GET /tasks/{task_id} → Get single task
@app.get("/tasks/{task_id}")
def get_single_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task 
    raise HTTPException(status_code=404, detail="Task not found")

#DELETE /tasks/{task_id}
@app.delete("/tasks/{task_id}")
def del_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task Deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
            
