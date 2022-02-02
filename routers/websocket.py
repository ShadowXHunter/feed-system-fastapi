from typing import List
from fastapi import APIRouter,Depends,WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import oauth2
from repository import feed

router = APIRouter(
    prefix="/ws",
    tags=['Websocket']
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager

@router.websocket('/')
async def websocket_endpoint(websocket: WebSocket, username: str = Depends(oauth2.get_current_user)):
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            await manager.send_personal_message(message, websocket)
            await manager.broadcast(f"{username}: {message}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)