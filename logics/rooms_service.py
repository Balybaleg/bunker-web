from models import Room, User
from storage import rooms, users
from typing import List
from logics.eventBus_service import EventBus

class RoomService:
    def __init__(self, event_bus: EventBus):
        self.rooms = rooms
        self.users = users
        self.event_bus = event_bus

    @staticmethod
    def event_handler(event_name):
        def decorator(func):
            func._event_name = event_name
            return func
        return decorator

    def _register_event_handlers(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, "_event_name"):
                self.event_bus.subscribe(attr._event_name, attr)


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
        return room

    async def delete_room(self, room_id: str) -> bool:
        for idx, r in enumerate(rooms):
            if r.room_id == room_id:
                del rooms[idx]
                await self.event_bus.publish("room_deleted", room_id)
                return True
        return False
    
    @event_handler("user_deleted")
    async def on_user_deleted(self, user_id: str):
        for room in rooms:
            if user_id in room.users:
                room.users.remove(user_id)


    async def turn_logic(self, room_id: str) -> bool:
        room : Room | None = self.get_room(room_id)
        if room:
            room_users : List[User] = [
                u for u in users 
                if (u.user_id in room.users and u.alive and u.user_id != room.room_admin) 
                or (not u.alive and u.is_my_turn)
                ]
            room_users.sort(key=lambda u: u.user_id)
            
            current_index = next((i for i, u in enumerate(room_users) if u.is_my_turn), None)
            for u in users:
                if u.user_id in room.users and not u.alive and u.is_my_turn:
                    u.is_my_turn = False
                    # current_index = current_index - 1
                    
            if current_index == None:
                room_users[0].is_my_turn = True
                # await broadcast(room_id, {"type": {"get_user_response" : await get_users(room_id)}})
                return True
            room_users[current_index].is_my_turn = False
            next_index = (current_index + 1) % len(room_users)
            room_users[next_index].is_my_turn = True

            # await broadcast(room_id, {"type": {"get_user_response" : await get_users(room_id)}})
            return True
