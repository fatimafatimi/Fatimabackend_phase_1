from websocket.manager import manager

async def task_created_event(task):
    message = {
        "type": "task_created",
        "task_id": task.id,
        "title": task.title,
        "project_id": task.project_id
    }
    await manager.broadcast(task.project_id, message)


async def task_updated_event(task):
    message = {
        "type": "task_updated",
        "task_id": task.id,
        "status": task.status,
        "project_id": task.project_id
    }
    await manager.broadcast(task.project_id, message)


async def task_deleted_event(task_id: int, project_id: int):
    message = {
        "type": "task_deleted",
        "task_id": task_id,
        "project_id": project_id
    }
    await manager.broadcast(project_id, message)