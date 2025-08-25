from fastapi import APIRouter, WebSocket

from server import ws_service

router = APIRouter(prefix= "/ws", tags=["ws"])

@router.websocket("/ws/{room_id}/{user_id}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str, username: str):
    return