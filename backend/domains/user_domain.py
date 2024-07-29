import datetime
import hashlib
from typing import Optional

import dto

from libs import dates
from models import user_model
from session import AsyncSessionLocal


async def create_user(
    db_session: AsyncSessionLocal, unsaved_user: dto.UnsavedUser
) -> dto.User:
    new_user = await user_model.create_user(db_session, unsaved_user)
    await db_session.commit()

    return new_user


async def find_one(
    db_session: AsyncSessionLocal, user_filter: dto.UserFilter
) -> Optional[dto.User]:
    return await user_model.find_one(db_session, user_filter)


async def auth_user(
    db_session: AsyncSessionLocal,
    auth_user: dto.AuthUser,
) -> Optional[dto.User]:

    verified_user = await user_model.find_one(
        db_session, dto.UserFilter(email=auth_user.email, password=auth_user.password)
    )

    return verified_user

async def generate_sha256_code(email):
    # Get the current time as a string
    current_time = datetime.datetime.now().isoformat()

    # Combine the email and current time
    combined_string = f"{email}{current_time}"

    # Encode the combined string to a bytes object
    encoded_string = combined_string.encode()

    # Create a new sha256 hash object and update it with the encoded string
    hash_object = hashlib.sha256()
    hash_object.update(encoded_string)

    # Get the hexadecimal representation of the hash
    hex_digest = hash_object.hexdigest()

    return hex_digest
