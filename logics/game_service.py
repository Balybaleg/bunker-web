from typing import Dict
from event_bus import EventBus
from logics.base_service import BaseService

class GameService(BaseService):
    def __init__(self, event_bus: EventBus, room_id: str):
        super().__init__(event_bus)
        self.room_id = room_id

    @BaseService.event_handler("game_action")
    async def on_game_action(self, action):
        return


class GameManager(BaseService):
    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)
        self.game_services : Dict[str, GameService] = {}

    async def get_game_service(self, room_id: str):
        game_service = self.game_services.get(room_id)
        if not game_service:
            return
        return game_service
    
    @BaseService.event_handler("room_event_bus_created")
    async def on_room_event_bus_created(self, data):
        for room_id, event_bus in data.items():
            self.game_services[room_id] = GameService(event_bus, room_id)
            await self.game_services[room_id].init()
        return self.game_services[room_id]
    
    @BaseService.event_handler("room_deleted")
    async def on_room_deleted(self, room_id: str):
        del self.game_services[room_id]
