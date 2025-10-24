from fastapi import APIRouter, WebSocket
from fastapi.responses import JSONResponse
from services import rooms_service, ws_manager, users_service

router = APIRouter(prefix= "/ws", tags=["ws"])

@router.websocket("/{room_id}/{user_id}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str, username: str):
    if await users_service.get_user(user_id):
        if await rooms_service.get_room(room_id):
            ws_serv = await ws_manager.get_ws_service(room_id)
            assert ws_serv is not None, "WsService должен существовать, если комната существует"
            await ws_serv.handle_connection(websocket,user_id)


@router.get("")
async def get_ws():
    return JSONResponse(str(ws_manager.ws_services))
