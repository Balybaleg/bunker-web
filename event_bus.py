class EventBus:
    def __init__(self, room_level: bool = False, room_id: str|None = None):
        self.subscribers = {}
        if room_level and not room_id:
            raise ValueError("room_id обязателен, когда room_level=True")
        if room_level:
            self.log_msg = f'[ROOM_BUS][{room_id}]'
        else:
            self.log_msg = '[GLOBAL_BUS]'

    async def subscribe(self, event_name: str, callback):
        callback_str = f"{callback.__self__.__class__.__name__}.{callback.__name__}"
        print(f"{self.log_msg}[LOG] Подписан {callback_str} -> event {event_name}")
        self.subscribers.setdefault(event_name, []).append(callback)

    async def unsubscribe(self, event_name: str, callback):
        callback_str = f"{callback.__self__.__class__.__name__}.{callback.__name__}"
        print(f"{self.log_msg}[LOG] Отписан {callback_str} -> event {event_name}")
        callbacks = self.subscribers.get(event_name)
        if callbacks and callback in callbacks:
            callbacks.remove(callback)
            if not callbacks:
                del self.subscribers[event_name]

    async def publish(self, event_name: str, data):
        print(f"{self.log_msg}[LOG] Опубликовано событие: {event_name}, данные: {data}")
        for callback in self.subscribers.get(event_name, []):
            callback_str = f"{callback.__self__.__class__.__name__}.{callback.__name__}"
            print(f"{self.log_msg}[LOG] Отправка события '{event_name}' обработчику: {callback_str}")
            await callback(data)
