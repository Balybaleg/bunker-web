from pydantic import BaseModel
from typing import Optional, List, Literal


class POSTResponse(BaseModel):
    username: str

class Room(BaseModel):
    room_id: str = None
    name: str | None = None
    room_admin: str | None = None
    users: List[str]  = []
    cards: dict | None = None  # Словарь с карточками, ключ - ID карточки, значение - объект Card
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
    card_owner: str | None = None  # ID пользователя, которому принадлежит карточка
    card: CardDetail

class User(BaseModel):
    user_id: str = None
    username: str
    room_id: str | None = None
    is_ready: bool = False
    is_admin: bool = False
    alive: bool = True
    is_my_turn: bool = False
    card_id: str | None = None  # ID карточки
    websocket_id: str | None = None
