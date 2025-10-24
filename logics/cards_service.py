
from event_bus import EventBus
from logics.base_service import BaseService

class CardsService(BaseService):
    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)
