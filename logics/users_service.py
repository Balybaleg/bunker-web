from models import Room, User
from storage import rooms, users
from typing import List
from logics.eventBus_service import EventBus

import uuid



class UserService:
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

    async def get_user(self, user_id: str):
        user = next((u for u in users if u.user_id == user_id))
        return user

    async def create_user(self, user : User):
        if not user.user_id:
            user.user_id = str(uuid.uuid4())        
        if user.room_id:
            room = next((r for r in rooms if r.room_id == user.room_id), None)
            if not room:
                return
            room.users.append(user.user_id)
        users.append(user)

    async def delete_user(self, user_id : str):
        for idx, u in enumerate(users):
            if u.user_id == user_id:
                del users[idx]
                await self.event_bus.publish("user_deleted", user_id)
                return True
        return False

    @event_handler("room_deleted")
    async def on_room_deleted(self, room_id: str):
        for user in users:
            if user.room_id == room_id:
                user.room_id = None
