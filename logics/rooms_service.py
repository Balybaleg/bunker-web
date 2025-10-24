from models import Room, User
from storage import rooms
from typing import List
from event_bus import EventBus
from logics.base_service import BaseService

class RoomService(BaseService):
    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)
        self.rooms = rooms

    async def get_room(self, room_id: str) -> Room | None:
        room = next((room for room in rooms if room.room_id == room_id), None)
        if room:
            return room
        return


    async def generate_room_id(self, length: int = 6) -> str:
        import random, string
        
        chars = string.ascii_uppercase + string.digits  # A-Z, 0-9
        while True:
            room_id = ''.join(random.choice(chars) for _ in range(length))
            # Проверяем уникальность
            if not any(r.room_id == room_id for r in rooms):
                return room_id
            
        
    async def create_room(self, username: str) -> Room:
        room_id = await self.generate_room_id()
        room = Room(
            room_id = room_id,
            name = f"Комната {len(rooms) + 1}",
            users = []
        )
        rooms.append(room)
        await self.event_bus.publish("room_created", room_id)
        return room

    async def delete_room(self, room_id: str) -> bool:
        for idx, r in enumerate(rooms):
            if r.room_id == room_id:
                del rooms[idx]
                await self.event_bus.publish("room_deleted", room_id)
                return True
        return False
    
    @BaseService.event_handler("user_deleted")
    async def on_user_deleted(self, user_id: str):
        for room in rooms:
            if user_id in room.users:
                room.users.remove(user_id)