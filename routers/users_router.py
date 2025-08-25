from fastapi import APIRouter, HTTPException
from models import User
from services import users_service

router = APIRouter(prefix= "/users", tags=["users"])



@router.get("")
async def get_users():
    return users_service.users

@router.get("/{user_id}")
async def get_user(user_id: str):
    user : User | None = await users_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Room not found")
    return user.model_dump_json()

@router.post("")
async def create_user(user: User):
    user : User = await users_service.create_user(user)
    return user.model_dump_json()


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    result : bool = await users_service.delete_user(user_id)
    if result:
        raise HTTPException(status_code=200, detail="User deleted")
    raise HTTPException(status_code=404, detail="User not found")