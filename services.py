from logics.eventBus_service import EventBus
from logics.users_service import UserService
from logics.rooms_service import RoomService


event_bus = EventBus()
users_service = UserService(event_bus)
rooms_service = RoomService(event_bus)