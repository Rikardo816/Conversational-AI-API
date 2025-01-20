from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        print("New connection accepted")
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        print("Connection closed")
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        try:
            print(f"Attempting to send: {message}")
            await websocket.send_text(message)
            print("Message sent successfully")
        except Exception as e:
            print(f"Error sending message: {e}")
