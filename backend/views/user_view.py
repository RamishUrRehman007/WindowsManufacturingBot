import dto
import serializers
from domains import user_domain
from fastapi import APIRouter, Depends, status
from models.common import get_db
from sqlalchemy.orm import Session
from views.common import get_current_user

router = APIRouter()


@router.post(
    "/users",
    response_model=dto.User,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
)
async def create_user(
    unsaved_user: dto.UnsavedUser,
    db_session: Session = Depends(get_db),
) -> dto.User:
    """
    Create view for creating a new User given an UnsavedUser payload.

    \f
    :return:
    """

    return await user_domain.create_user(db_session, unsaved_user)


@router.get(
    "/users",
    response_model=dto.PagedResult[dto.User],
    tags=["users"],
)
async def get_users(
    page: dto.Page = Depends(serializers.page_from_query_param),
    current_user: dto.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
) -> dto.PagedResult[dto.User]:
    """
    List view for getting Users.
    \f
    :return:
    """
    return await user_domain.find_many(
        db_session,
        dto.UserFilter(
            user_id=None if current_user.is_root else current_user.id, page=page
        ),
    )


@router.get(
    "/me",
    response_model=dto.User,
    tags=["users"],
)
async def get_current_user_info(
    current_user: dto.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
) -> dto.User:
    return await user_domain.find_one(
        db_session=db_session, user_filter=dto.UserFilter(user_id=current_user.id)
    )
