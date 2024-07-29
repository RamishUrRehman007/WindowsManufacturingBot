from typing import Optional

import dto
from exceptions import ChatNotFoundError
from models import chat_model
from session import AsyncSessionLocal


async def create_chat(
    db_session: AsyncSessionLocal,
    user_id: dto.UserID,
    unsaved_chat: dto.UnsavedChat,
) -> dto.Chat:
    new_chat = await chat_model.create_chat(
        db_session, dto.UnsavedChat(chat_name=unsaved_chat.chat_name, user_id=user_id)
    )

    await db_session.commit()

    return new_chat


async def find_one(
    db_session: AsyncSessionLocal, chat_filter: dto.ChatFilter
) -> Optional[dto.Chat]:
    return await chat_model.find_one(db_session, chat_filter)


async def find_many(
    db_session: AsyncSessionLocal, chat_filter: dto.ChatFilter
) -> dto.PagedResult[dto.Chat]:
    return await chat_model.find_many(db_session, chat_filter)
