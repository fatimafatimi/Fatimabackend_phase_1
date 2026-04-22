from fastapi import WebSocket
from typing import Dict, List


class ConnectionManager:
    def __init__(self):
        # { project_id: [websocket1, websocket2] }
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, project_id: int, websocket: WebSocket):
        await websocket.accept()

        if project_id not in self.active_connections:
            self.active_connections[project_id] = []

        self.active_connections[project_id].append(websocket)

    def disconnect(self, project_id: int, websocket: WebSocket):
        if project_id in self.active_connections:
            self.active_connections[project_id].remove(websocket)

            if not self.active_connections[project_id]:
                del self.active_connections[project_id]

    async def broadcast(self, project_id: int, message: dict):
        if project_id in self.active_connections:
            for connection in self.active_connections[project_id][:]:  # copy list
                try:
                    await connection.send_json(message)
                except:
                    self.active_connections[project_id].remove(connection)


# global instance (IMPORTANT)
manager = ConnectionManager()