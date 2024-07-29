import dto
from domains import user_domain
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from models.common import get_db
from session import AsyncSessionLocal
from sqlalchemy.orm import Session


async def get_current_user(
    authorize: AuthJWT = Depends(), db_session: Session = Depends(get_db)
) -> dto.User:
    authorize.jwt_required()
    user = await user_domain.find_one(
        db_session, dto.UserFilter(user_id=authorize.get_jwt_subject())
    )
    assert user

    return user