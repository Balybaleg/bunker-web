from pydantic import BaseModel
from typing import List
import uuid


class POSTResponse(BaseModel):
    username: str

class Room(BaseModel):
    room_id: str | None = None
    name: str | None = None
    users: List[str]  = []
    cards: dict | None = None
    game_id: str | None = None
    is_game_started: bool = False

class CardParam(BaseModel):
    value: str
    revealed: bool = False

class CardDetail(BaseModel):
    bio: CardParam
    profession: CardParam
    hobby: CardParam
    health: CardParam
    phobia: CardParam
    inventory: CardParam
    advance: CardParam

class Card(BaseModel):
    card_id: str
    card_owner: str | None = None
    card: CardDetail

class User(BaseModel):
    user_id: str | None = None
    username: str
    room_id: str | None = None
    is_ready: bool = False
    is_admin: bool = False
    alive: bool = True
    is_my_turn: bool = False
    card_id: str | None = None
    websocket_id: str | None = None

class Game(BaseModel):
    game_id: str = str(uuid.uuid4())
    room_id: str
    state: str = "waiting"
    game_admin: User
    players: List[User]
