from typing import Any, Dict, Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.background import BackgroundTasks
from starlette.responses import Response

from src.auth import service, jwt, utils
from src.auth.dependencies import valid_refresh_token, valid_refresh_token_user
from src.auth.schemas import AccessTokenResponse, AuthUser

router = APIRouter()


@router.post("/login", response_model=AccessTokenResponse)
async def auth_user(auth_data: AuthUser) -> AccessTokenResponse:
    user = await service.authenticate_user(auth_data)
    refresh_token_value = await service.create_refresh_token(user_id=user["id"])

    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
        user=user
    )


@router.put("/tokens", response_model=AccessTokenResponse)
async def refresh_tokens(
        worker: BackgroundTasks,
        response: Response,
        refresh_token: dict[str, Any] = Depends(valid_refresh_token),
        user: dict[str, Any] = Depends(valid_refresh_token_user),
) -> AccessTokenResponse:
    refresh_token_value = await service.create_refresh_token(
        user_id=refresh_token["user_id"]
    )
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    worker.add_task(service.expire_refresh_token, refresh_token["id"])
    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
        user=user
    )


@router.post("/swagger/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await service.authenticate_user_swagger(form_data.username, form_data.password)
    refresh_token_value = await service.create_refresh_token(user_id=user["id"])

    return {"access_token": jwt.create_access_token(user=user), "token_type": "bearer",
            "refresh_token": refresh_token_value, "user": user}
