from models import Room, User
from storage import rooms, users
from typing import List
from event_bus import EventBus
from logics.base_service import BaseService

import uuid



class UserService(BaseService):
    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)
        self.rooms = rooms
        self.users = users

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
        return user

    async def delete_user(self, user_id : str):
        for idx, u in enumerate(users):
            if u.user_id == user_id:
                del users[idx]
                await self.event_bus.publish("user_deleted", user_id)
                return True
        return False

    @BaseService.event_handler("room_deleted")
    async def on_room_deleted(self, room_id: str):
        for user in users:
            if user.room_id == room_id:
                user.room_id = None
