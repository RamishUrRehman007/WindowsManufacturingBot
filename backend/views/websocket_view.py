import json
import dto
from dependencies.websocket.redisManager import RedisPubSubManager
from dependencies.websocket.socketManager import WebSocketManager
from domains import chat_domain, message_domain
from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
)
from models.common import get_db
from sqlalchemy.orm import Session

router = APIRouter()


# Create an instance of RedisPubSubManager
pubsub_client = RedisPubSubManager()
# Pass the instance directly to WebSocketManager
socket_manager = WebSocketManager(pubsub_client=pubsub_client)


@router.websocket("/websockets/{chat_id}/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: str,
    user_id: int,
    db_session: Session = Depends(get_db),
):
    await socket_manager.add_user_to_room(chat_id, websocket)
    message = {
        "user_id": user_id,
        "chat_id": chat_id,
        "message": f"User {user_id} connected to chat - {chat_id}"
    }
    await socket_manager.broadcast_to_room(chat_id, json.dumps(message))
    try:
        while True:
            data = await websocket.receive_text()
            message = {
                "user_id": user_id,
                "chat_id": chat_id,
                "message": data
            }
            await socket_manager.broadcast_to_room(chat_id, json.dumps(message))
            import logging
            logging.info(data)
            logging.info(type(data))

            json_data = json.loads(data)
            await message_domain.create_message(
                db_session,
                user_id,
                dto.UnsavedMessage(
                    chat_id=chat_id,
                    user_id=user_id,
                    message=json_data["message"],
                ),
            )

    except WebSocketDisconnect:
        await socket_manager.remove_user_from_room(chat_id, websocket)

        message = {
            "user_id": user_id,
            "chat_id": chat_id,
            "message": f"User {user_id} disconnected from chat - {chat_id}"
        }
        await socket_manager.broadcast_to_room(chat_id, json.dumps(message))
