from typing import Optional

import dto
from exceptions import DuplicateChatError
from models.common import Chat, result_to_chat
from session import AsyncSessionLocal
from sqlalchemy import exc, select
from sqlalchemy.orm import Query


async def create_chat(
    db_session: AsyncSessionLocal,
    unsaved_chat: dto.UnsavedChat,
) -> dto.Chat:
    chat = Chat(**unsaved_chat.dict())
    db_session.add(chat)
    try:
        await db_session.flush()
    except exc.IntegrityError:
        await db_session.rollback()
        raise DuplicateChatError(
            f"Chat with name {unsaved_chat.chat_name} already exists."
        )

    new_chat = await find_one(
        db_session, dto.ChatFilter(chat_id=dto.ChatID(chat.id))
    )
    assert new_chat

    return new_chat


async def find_many(
    db_session: AsyncSessionLocal, chat_filter: dto.ChatFilter
) -> dto.PagedResult[dto.Chat]:
    query = select(Chat).order_by(Chat.id.desc())
    query = _filter_to_query(query, chat_filter)

    print(query)

    results = await db_session.execute(query)

    return dto.PagedResult(
        results=[result_to_chat(result[0]) for result in results]
    )


async def find_one(
    db_session: AsyncSessionLocal, chat_filter: dto.ChatFilter
) -> Optional[dto.Chat]:
    query = select(Chat)
    query = _filter_to_query(query, chat_filter)

    result = await db_session.execute(query)

    rows = result.one_or_none()
    if rows is None:
        return None

    return result_to_chat(rows[0])



def _filter_to_query(query: Query, chat_filter: dto.ChatFilter) -> Query:
    if chat_filter.chat_id:
        query = query.where(Chat.id == chat_filter.chat_id)

    if chat_filter.chat_name:
        query = query.where(Chat.chat_name == chat_filter.chat_name)


    if chat_filter.user_id:
        query = query.where(Chat.user_id == chat_filter.user_id)

    if chat_filter.page:
        query = query.limit(chat_filter.page.size).offset(
            chat_filter.page.offset
        )

    query = query.where(Chat.deleted_at == None)  # noqa: E711

    return query
