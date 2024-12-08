from fastapi import WebSocket
import asyncio
from interfaces import NotificationService
import json

class WebSocketNotificationService(NotificationService):
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_notification(self, session_id: str, products: list):
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(json.dumps(products))
            except Exception as e:
                print(f"Failed to send notification to {session_id}: {str(e)}")
