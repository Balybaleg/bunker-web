import asyncio
from event_bus import EventBus
from logics.eventBus_service import EventBusManager
from logics.users_service import UserService
from logics.rooms_service import RoomService
from logics.ws_service import WsManager
from logics.game_service import GameManager

event_bus = EventBus() # глобальная шина событий
event_bus_manager = EventBusManager(event_bus) # сервис для управления локальными шинами событий
users_service =  UserService(event_bus)
rooms_service =  RoomService(event_bus)
ws_manager =  WsManager(event_bus)
games_manager = GameManager(event_bus)

async def init_all():
    await event_bus_manager.init()
    await users_service.init()
    await rooms_service.init()
    await ws_manager.init()
    await games_manager.init()

asyncio.create_task(init_all())
