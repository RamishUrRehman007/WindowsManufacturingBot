from typing import Optional
import logging
import dto
from arq.connections import create_pool
from config import REDIS_SETTINGS
from models import message_model
from session import AsyncSessionLocal
from dependencies.llm_service import OpenAIModel 
import json
from dependencies.websocket.redisManager import RedisPubSubManager
from config import OPEN_AI_API_KEY, OPEN_AI_MODEL
from constants import llm_instructions

async def create_message(
    db_session: AsyncSessionLocal,
    user_id: dto.UserID,
    unsaved_message: dto.UnsavedMessage,
) -> dto.Message:
    new_message = await message_model.create_message(db_session, unsaved_message)

    await db_session.commit()

    redis = await create_pool(REDIS_SETTINGS)
    job = await redis.enqueue_job(
        "process_message_to_llm",
        new_message.id,
        new_message.chat_id,
    )

    job_id_str = str(job)
    job_id = job_id_str.split(" ")[2][:-1]

    return new_message


async def find_one(
    db_session: AsyncSessionLocal, message_filter: dto.MessageFilter
) -> Optional[dto.Message]:
    return await message_model.find_one(db_session, message_filter)


async def find_many(
    db_session: AsyncSessionLocal, message_filter: dto.MessageFilter
) -> dto.PagedResult[dto.Message]:
    return await message_model.find_many(db_session, message_filter)


async def process_message_to_llm(
    db_session: AsyncSessionLocal,
    message_id: dto.MessageID,
    chat_id: dto.ChatID,
) -> dto.Message:

    message = await message_model.find_one(
        db_session,
        dto.MessageFilter(
            message_id=message_id
        ),
    )
    logging.info(f"Message to send Open AI: {message}")
    openai_model = OpenAIModel(api_key=OPEN_AI_API_KEY, model=OPEN_AI_MODEL) 

    db_messages = await message_model.find_many(
        db_session,
        dto.MessageFilter(
            chat_id=chat_id,
            limit=10,
        ),
    )
    messages = []
    for db_message in db_messages.results:
        if db_message.user_id == 1:
            messages.append(openai_model.format_ai_template(db_message.message))
        else:
            messages.append(openai_model.format_human_template(db_message.message))



    open_ai_message = await openai_model.send_prompt_to_llm(message.message, llm_instructions, messages
    )
    await message_model.create_message(
        db_session,
        dto.UnsavedMessage(
            chat_id=chat_id,
            user_id=1,
            message=open_ai_message,
        ),
    )

    logging.info(f"Open AI message: {open_ai_message}")

    pubsub_manager = RedisPubSubManager()
    await pubsub_manager.connect()
    message = {
        "user_id": 1,
        "chat_id": chat_id,
        "message": open_ai_message,
    }
    message_json = json.dumps(message)
    logging.info(f"Message from openai: {message}")
    await pubsub_manager.publish(chat_id, message_json)

    await db_session.commit()