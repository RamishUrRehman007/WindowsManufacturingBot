from typing import Optional

import dto
import serializers
from domains import chat_domain
from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    status,
)
from models.common import get_db
from session import AsyncSessionLocal
from sqlalchemy.orm import Session
from views.common import get_current_user

router = APIRouter()


@router.post(
    "/chats",
    response_model=dto.Chat,
    status_code=status.HTTP_201_CREATED,
    tags=["chats"],
)
async def create_chat(
    unsaved_chat: dto.UnsavedChat,
    current_user: dto.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
) -> dto.Chat:
    """
    Create view for creating a new Chat given an UnsavedChat payload.

    \f
    :return:
    """

    return await chat_domain.create_chat(
        db_session, user_id=current_user.id, unsaved_chat=unsaved_chat
    )


@router.get(
    "/chats",
    response_model=dto.PagedResult[dto.Chat],
    tags=["chats"],
)
async def get_chats(
    chat_id: Optional[dto.ChatID] = Query(
        None,
        title="Chat ID",
        description="The ID of the Chat",
    ),
    chat_name: Optional[str] = Query(
        None,
        title="Chat Name",
        description="The Name of the Chat",
    ),
    user_id: Optional[dto.UserID] = Query(
        None,
        title="Base User ID",
        description="The ID of the Base User",
    ),
    page: dto.Page = Depends(serializers.page_from_query_param),
    current_user: dto.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
) -> dto.PagedResult[dto.Chat]:
    """
    List view for getting Chats.
    \f
    :return:
    """

    return await chat_domain.find_many(
        db_session,
        dto.ChatFilter(
            chat_id=chat_id,
            chat_name=chat_name,
            base_user_id=user_id,
            only_students=True,
            page=page,
        ),
    )


@router.get(
    "/chats/{chat_id}",
    response_model=dto.Chat,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": dto.ErrorResponse,
            "description": "Chat not found.",
        },
    },
    tags=["chats"],
)
async def get_chat(
    chat_id: dto.ChatID = Path(
        ...,
        title="Chat ID",
        description="The ID of the Chat to get.",
    ),
    current_user: dto.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
) -> dto.Chat:
    """
    Detail view for getting one Chat by ID.

    \f
    :return:
    """
    return await chat_domain.find_one(
        db_session,
        dto.ChatFilter(
            chat_id=chat_id,
        ),
    )