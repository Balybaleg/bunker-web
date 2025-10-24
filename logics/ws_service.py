import asyncio
from event_bus import EventBus
from fastapi import WebSocket, websockets
from fastapi.websockets import WebSocketDisconnect
from typing import List
from typing import Dict
from logics.base_service import BaseService


class WsConnection(BaseService):
    def __init__(self, event_bus: EventBus, websocket: WebSocket, user_id: str):
        super().__init__(event_bus)
        self._websocket = websocket
        self.user_id = user_id
        self.closed = False

    async def accept(self):
        await self._websocket.accept()

    async def send(self, message: str):
        if not self.closed:
            await self._websocket.send_text(message)

    async def close(self, code: int = 1000):
        await self._websocket.close(code)
        self.closed = True

    async def receive_loop(self):
        if not self.closed:
            try:
                while True:
                    data = await self._websocket.receive_text()
                    await self.event_bus.publish("ws_msg_received", {"user_id": self.user_id, "msg": data})
            except WebSocketDisconnect:
                self.closed = True
                return

class WsService(BaseService):
    def __init__(self, event_bus: EventBus, room_id: str):
        # websocket: WebSocket, room_id: str, user_id: str, username: str
        super().__init__(event_bus)
        self.connections: Dict[str, WsConnection] = {}

    async def get_connection(self, user_id: str):
        return self.connections[user_id]

    async def connect(self, websocket: WebSocket, user_id: str):
        connection = WsConnection(self.event_bus, websocket, user_id)
        await connection.init()
        self.connections[user_id] = connection
        data = {
            "user_id" : user_id,
        }
        await connection.accept()
        await self.event_bus.publish("user_connected", data)
        return connection
    
    async def disconnect(self, user_id: str):
        connection: WsConnection = await self.get_connection(user_id)
        if not connection.closed:
            await connection.close()
        del self.connections[user_id]
        data = {
            "user_id" : connection.user_id,
        }
        await self.event_bus.publish("user_disconnected", data)

    async def handle_connection(self, websocket: WebSocket, user_id: str):
        connection = await self.connect(websocket, user_id)
        try:
            await connection.receive_loop()
        finally:
            await self.disconnect(user_id)

    async def broadcast(self, msg: str, exclude: List[str]|None = None):
        if exclude is None:
            exclude = []
        for user_id, conn in self.connections.items():
            if user_id not in exclude:
                await conn.send(msg)

    @BaseService.event_handler("ws_msg_received")
    async def on_ws_msg_received(self, msg):
        print(msg)
        return

class WsManager(BaseService):
    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)
        self.ws_services : Dict[str, WsService] = {}

    async def get_ws_service(self, room_id: str):
        ws_service = self.ws_services.get(room_id)
        if not ws_service:
            return
        return ws_service

    
    @BaseService.event_handler("room_event_bus_created")
    async def on_room_event_bus_created(self, data):
        for room_id, event_bus in data.items():
            self.ws_services[room_id] = WsService(event_bus, room_id)
            await self.ws_services[room_id].init()
        return self.ws_services[room_id]

    @BaseService.event_handler("room_deleted")
    async def on_room_deleted(self, room_id: str):
        del self.ws_services[room_id]
    