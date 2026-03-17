from fastapi import HTTPException, APIRouter, status
from models.task import tasks, current_id
from schemas.task_schema import TaskCreate, TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# GET all tasks
@router.get("/", response_model=list[TaskResponse])
def get_tasks():
    return tasks


# POST create task
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    task_dict = task.dict()
    task_dict["id"] = current_id["value"]
    tasks.append(task_dict)
    current_id["value"] += 1
    return task_dict


# GET single task
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )


# DELETE task
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )