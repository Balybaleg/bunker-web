class EventBus:
    def __init__(self):
        self.subscribers = {}

    async def subscribe(self, event_name: str, callback):
        """Подписываем обработчик на событие"""
        self.subscribers.setdefault(event_name, []).append(callback)

    async def publish(self, event_name: str, data):
        """Публикуем событие"""
        for callback in self.subscribers.get(event_name, []):
            callback(data)
