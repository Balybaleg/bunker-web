from typing import Dict, List

from logics.base_service import BaseService
from event_bus import EventBus


class EventBusManager(BaseService):
    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)
        self.local_buses: Dict[str, EventBus] = {}


    async def get_local_bus(self, room_id: str):
        local_bus = self.local_buses.get(room_id)
        if not local_bus:
            return None
        return local_bus

    @BaseService.event_handler("room_created")
    async def on_room_created(self, room_id: str):
        self.local_buses[room_id] = EventBus(room_level = True, room_id= room_id)
        data = {}
        data[room_id] = self.local_buses[room_id]
        await self.event_bus.publish("room_event_bus_created", data)
        return self.local_buses[room_id]
    
