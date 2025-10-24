from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import rooms_router, users_router, ws_router
# from logics.eventBus_service import EventBus
# from logics.users_service import UserService
# from logics.rooms_service import RoomService
# from logics.cards_service import CardsService
# from logics.game_service import GameService
# from logics.ws_service import WsService


# event_bus = EventBus()
# usersService = UserService(event_bus)
# roomsService = RoomService(event_bus)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms_router.router)
app.include_router(users_router.router)
# app.include_router(cards_router.router)
app.include_router(ws_router.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
