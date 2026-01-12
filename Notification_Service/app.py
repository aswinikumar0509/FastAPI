from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="Notification Service")

class NotificationCreate(BaseModel):
    user:str
    message:str

class ConnectionManager:

    def __init__(self):
        self.active_connections: Dict[str , List[WebSocket]] = {}

    async def connect(self, user:str, Websocket: WebSocket):
        await Websocket.accept()
        self.active_connections.setdefault(user,[]).append(Websocket)

    def disconnect(self,user: str, websocket: WebSocket):
        conns = self.active_connections.get(user,[])
        if websocket in conns:
            conns.remove(websocket)
        
    async def send_to_user(self,user:str, message:str):
        conns = self.active_connections.get(user,[])
        for ws in conns:
            await ws.send_text(message)