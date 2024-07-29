from typing import Optional

import dto
import serializers
from domains import message_domain
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
    "/messages",
    response_model=dto.Message,
    status_code=status.HTTP_201_CREATED,
    tags=["messages"],
)
async def create_message(
    unsaved_message_request: dto.UnsavedMessageRequest,
    current_user: dto.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
) -> dto.Message:
    """
    Create view for creating a new Message given an UnsavedMessage payload.

    \f
    :return:
    """

    return await message_domain.create_message(
        db_session,
        user_id=current_user.id,
        unsaved_message=dto.UnsavedMessage(**unsaved_message_request.dict()),
    )


@router.get(
    "/messages",
    response_model=dto.PagedResult[dto.Message],
    tags=["messages"],
)
async def get_messages(
    chat_id: Optional[dto.ChatID] = Query(
        None,
        title="Chat ID",
        description="The ID of the Chat",
    ),
    user_id: Optional[dto.UserID] = Query(
        None,
        title="User ID",
        description="The ID of the User",
    ),
    message: Optional[str] = Query(
        None,
        title="Message",
        description="Message.....",
    ),
    page: dto.Page = Depends(serializers.page_from_query_param),
    current_user: dto.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
) -> dto.PagedResult[dto.Message]:
    """
    List view for getting Messages.
    \f
    :return:
    """

    return await message_domain.find_messages_with_ai_interactions(
        db_session,
        dto.MessageFilter(
            chat_id=chat_id,
            user_id=user_id,
            message=message,
            page=page,
        ),
    )


@router.get(
    "/messages/{message_id}",
    response_model=dto.Message,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": dto.ErrorResponse,
            "description": "Message not found.",
        },
    },
    tags=["messages"],
)
async def get_message(
    message_id: dto.MessageID = Path(
        ...,
        title="Message ID",
        description="The ID of the Message to get.",
    ),
    current_user: dto.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
) -> dto.Message:
    """
    Detail view for getting one Message by ID.

    \f
    :return:
    """
    return await message_domain.find_one(
        db_session,
        dto.MessageFilter(
            message_id=message_id,
        ),
    )
