import json
import uuid
from typing import Any

import dto
from session import AsyncSessionLocal
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()  # type: Any


async def get_db() -> AsyncSessionLocal:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(Text)
    user_name = Column(Text)
    hashed_password = Column(Text)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    deleted_at = Column(DateTime(timezone=True))


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    chat_name = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    deleted_at = Column(DateTime(timezone=True))


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    message_status = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )


def result_to_user(result: User) -> dto.User:
    return dto.User(
        id=dto.UserID(result.id),
        user_name=result.user_name,
        email=result.email,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )


def result_to_chat(result: Chat) -> dto.Chat:
    return dto.Chat(
        id=dto.ChatID(result.id),
        chat_name=result.chat_name,
        user_id=dto.UserID(result.user_id),
        created_at=result.created_at,
        updated_at=result.updated_at,
    )


def result_to_message(result: Message) -> dto.Message:
    return dto.Message(
        id=dto.MessageID(result.id),
        chat_id=result.chat_id,
        user_id=dto.UserID(result.user_id),
        message=result.message,
        message_status=result.message_status,
        created_at=result.created_at,
    )
