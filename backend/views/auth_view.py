import json
import logging

import dto
from domains import user_domain
from fastapi import APIRouter, Depends, HTTPException, responses, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from models.common import get_db
from sqlalchemy.orm import Session
from views.common import get_current_user

router = APIRouter()


@router.post(
    "/auth/login",
    response_model=dto.AuthToken,
    status_code=status.HTTP_200_OK,
    tags=["auth"],
)
async def login(
    auth_user: dto.AuthUser,
    db_session: Session = Depends(get_db),
    authorize: AuthJWT = Depends(),
) -> dto.AuthToken:
    """
    Auth view for generating auth tokens given an AuthUser payload.

    \f
    :return:
    """

    user = await user_domain.auth_user(db_session, auth_user)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )


    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Login Successfully",
            "user": json.loads(user.json()),
            "access_token": authorize.create_access_token(subject=user.id),
            "refresh_token": authorize.create_refresh_token(subject=user.id)
        },
    )

    return response


@router.post(
    "/auth/refresh",
    status_code=status.HTTP_200_OK,
    tags=["auth"],
)
async def refresh_token(authorize: AuthJWT = Depends()) -> dto.AuthToken:
    """
    Auth view for regenerating auth tokens using refresh token.

    \f
    :return:
    """
    authorize.jwt_refresh_token_required()
    return dto.AuthToken(
        otp=False,
        access_token=authorize.create_access_token(subject=authorize.get_jwt_subject()),
    )


@router.post(
    "/auth/logout",
    response_class=responses.Response,
    status_code=status.HTTP_200_OK,
    tags=["auth"],
)
async def logout(
    current_user: dto.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
) -> dto.AuthToken:
    """
    Auth view for logging out user.

    \f
    :return:
    """

    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Log Out",
        },
    )

    response.set_cookie(key="access_token", value="", max_age=0)
    response.set_cookie(key="refresh_token", value="", max_age=0)

    return response
