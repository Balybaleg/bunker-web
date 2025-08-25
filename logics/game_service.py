


from v2.logics.eventBus_service import EventBus

class GameService:
    async def __init__(self, event_bus: EventBus):


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