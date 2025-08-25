from fastapi import APIRouter, HTTPException
from models import Room, POSTResponse
from services import rooms_service

router = APIRouter(prefix= "/rooms", tags=["rooms"])


@router.get("")
async def get_rooms():
    return rooms_service.rooms

@router.get("/{room_id}")
async def get_room(room_id: str):
    room : Room | None = await rooms_service.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room.model_dump_json()

@router.post("")
async def create_room(response: POSTResponse):
    room : Room = await rooms_service.create_room(response.username)
    return room.model_dump_json()


@router.delete("/{room_id}")
async def delete_room(room_id: str):
    result : bool = await rooms_service.delete_room(room_id)
    if result:
        raise HTTPException(status_code=200, detail="Room deleted")
    raise HTTPException(status_code=404, detail="Room not found")