from typing import Optional

import dto
from models.common import Message, result_to_message
from session import AsyncSessionLocal
from sqlalchemy import exc, select
from sqlalchemy.orm import Query
from exceptions import DuplicateEntityError

async def create_message(
    db_session: AsyncSessionLocal, unsaved_message: dto.UnsavedMessage
) -> dto.Message:
    message = Message(**unsaved_message.dict())
    db_session.add(message)
    try:
        await db_session.flush()
    except exc.IntegrityError:
        await db_session.rollback()
        raise DuplicateEntityError(
            f"Message with name {unsaved_message} already exists."
        )

    new_message = await find_one(
        db_session, dto.MessageFilter(message_id=dto.MessageID(message.id))
    )
    assert new_message

    return new_message


async def find_many(
    db_session: AsyncSessionLocal, message_filter: dto.MessageFilter
) -> dto.PagedResult[dto.Message]:
    query = select(Message).order_by(Message.id.asc())
    query = _filter_to_query(query, message_filter)

    results = await db_session.execute(query)

    return dto.PagedResult(results=[result_to_message(result[0]) for result in results])


async def find_one(
    db_session: AsyncSessionLocal, message_filter: dto.MessageFilter
) -> Optional[dto.Message]:
    query = select(Message)
    query = _filter_to_query(query, message_filter)

    result = await db_session.execute(query)

    rows = result.one_or_none()
    if rows is None:
        return None

    return result_to_message(rows[0])


def _filter_to_query(query: Query, message_filter: dto.MessageFilter) -> Query:
    if message_filter.message_id:
        query = query.where(Message.id == message_filter.message_id)


    if message_filter.chat_id:
        query = query.where(Message.chat_id == message_filter.chat_id)

    if message_filter.user_id:
        query = query.where(Message.user_id == message_filter.user_id)
    
    if message_filter.limit:
        query = query.limit(message_filter.limit)

    if message_filter.page:
        query = query.limit(message_filter.page.size).offset(message_filter.page.offset)


    return query
