from datetime import datetime
from typing import Any, Dict, Generic, List, NewType, Optional, TypeVar, Union

from pydantic import BaseModel, EmailStr, PositiveInt
from pydantic.generics import GenericModel

ResponseT = TypeVar("ResponseT")
UserID = NewType("UserID", int)
ChatID = NewType("ChatID", int)
MessageID = NewType("MessageID", int)

JSON = Dict[str, Any]
UNION = Union

class Page(BaseModel):
    number: Optional[PositiveInt] = None
    size: Optional[PositiveInt] = None
    offset: int


class PagedResult(GenericModel, Generic[ResponseT]):
    results: List[ResponseT]
    total_count: Optional[int] = 0


class ErrorResponse(BaseModel):
    detail: str


# Users Models

class UnsavedUser(BaseModel):
    user_name: str
    email: EmailStr
    password: str


class User(BaseModel):
    id: UserID
    user_name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class UserFilter(BaseModel):
    user_id: Optional[UserID] = None
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


# Chats Models

class UnsavedChat(BaseModel):
    chat_name: str
    user_id: Optional[UserID]


class Chat(UnsavedChat):
    id: ChatID
    created_at: datetime
    updated_at: datetime


class ChatFilter(BaseModel):
    chat_id: Optional[ChatID] = None
    user_id: Optional[UserID] = None
    chat_name: Optional[str] = None
    page: Optional[Page] = None


# Messages Models

class UnsavedMessageRequest(BaseModel):
    chat_id: ChatID
    user_id: UserID
    message: str


class UnsavedMessage(UnsavedMessageRequest):
    message_status: str = "INPROGRESS"


class Message(BaseModel):
    id: MessageID
    chat_id: ChatID
    user_id: UserID
    message: str 
    created_at: datetime

class MessageFilter(BaseModel):
    message_id: Optional[MessageID] = None
    chat_id: Optional[ChatID] = None
    user_id: Optional[UserID] = None
    message_status: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[Page] = None


# Auth Models

class AuthUser(BaseModel):
    email: str
    password: str
    otp: Optional[str]


class AuthToken(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]
    otp: bool
    is_root: Optional[bool] = False
