from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websocket.manager import manager

router = APIRouter()


@router.websocket("/ws/project/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: int):
    await manager.connect(project_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            message = {
                "type": "chat",
                "user": data.get("user", "Anonymous"),
                "message": data.get("message")
            }

            await manager.broadcast(project_id, message)

    except WebSocketDisconnect:
        manager.disconnect(project_id, websocket)