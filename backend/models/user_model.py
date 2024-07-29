from typing import Optional

import dto
from exceptions import DuplicateUserError
from models.common import User, result_to_user
from passlib.context import CryptContext
from session import AsyncSessionLocal
from sqlalchemy import exc, select
from sqlalchemy.orm import Query

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(
    db_session: AsyncSessionLocal, unsaved_user: dto.UnsavedUser
) -> dto.User:
    user = User(
        **unsaved_user.dict(exclude={"password"}),
        hashed_password=pwd_context.hash(unsaved_user.password),
    )
    db_session.add(user)
    try:
        await db_session.flush()
    except exc.IntegrityError:
        await db_session.rollback()
        raise DuplicateUserError(
            f"User with email {unsaved_user.email} already exists."
        )

    new_user = await find_one(db_session, dto.UserFilter(user_id=dto.UserID(user.id)))
    assert new_user

    return new_user


async def find_many(
    db_session: AsyncSessionLocal, user_filter: dto.UserFilter
) -> dto.PagedResult[dto.User]:
    query = select(User).order_by(User.id.desc())
    query = _filter_to_query(query, user_filter)

    results = await db_session.execute(query)

    return dto.PagedResult(results=[result_to_user(result[0]) for result in results])


async def find_one(
    db_session: AsyncSessionLocal, user_filter: dto.UserFilter
) -> Optional[dto.User]:
    query = select(User)
    query = _filter_to_query(query, user_filter)

    result = await db_session.execute(query)

    rows = result.one_or_none()
    if rows is None:
        return None

    return (
        _verify_password(rows[0], user_filter.password)
        if user_filter.password
        else result_to_user(rows[0])
    )


def _verify_password(result: User, password: str) -> Optional[dto.User]:
    return (
        result_to_user(result)
        if pwd_context.verify(password, result.hashed_password)
        else None
    )


def _filter_to_query(query: Query, user_filter: dto.UserFilter) -> Query:
    if user_filter.user_id:
        query = query.where(User.id == user_filter.user_id)

    if user_filter.email:
        query = query.where(User.email == user_filter.email)

    query = query.where(User.deleted_at == None)  # noqa: E711

    return query
