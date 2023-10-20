import uuid
from datetime import datetime, timedelta
from typing import Any

from pydantic import UUID4

from database.connection import execute, fetch_one
from src import utils
from src.app.service import get_user_by_username
from src.auth.config import auth_config
from src.auth.exceptions import InvalidCredentials
from src.auth.models import refresh_tokens
from src.auth.schemas import AuthUser
from src.auth.security import check_password


async def create_refresh_token(
        *, user_id: int, refresh_token: str | None = None
) -> str:
    if not refresh_token:
        refresh_token = utils.generate_random_alphanum(64)

    insert_query = refresh_tokens.insert().values(
        refresh_token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
        user_id=user_id,
    )
    await execute(insert_query)

    return refresh_token


async def get_refresh_token(refresh_token: str) -> dict[str, Any] | None:
    select_query = refresh_tokens.select().where(
        refresh_tokens.c.refresh_token == refresh_token
    )

    return await fetch_one(select_query)


async def expire_refresh_token(refresh_token_id: int) -> None:
    update_query = (
        refresh_tokens.update()
        .values(expires_at=datetime.utcnow() - timedelta(days=1))
        .where(refresh_tokens.c.id == refresh_token_id)
    )

    await execute(update_query)


async def authenticate_user(auth_data: AuthUser) -> dict[str, Any]:
    user = await get_user_by_username(auth_data.username)
    if not user:
        raise InvalidCredentials()

    if not check_password(auth_data.password, user["password"]):
        raise InvalidCredentials()

    return user


async def authenticate_user_swagger(username: str, password: str) -> dict[str, Any]:
    user = await get_user_by_username(username)
    if not user:
        raise InvalidCredentials()

    if not check_password(password, user["password"]):
        raise InvalidCredentials()

    return user


# async def get_current_user(token: str = Depends(reuseable_oauth)) -> User:
#     try:
#         payload = jwt.decode(
#             token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
#         )
#         token_data = TokenPayload(**payload)
#
#         if datetime.fromtimestamp(token_data.exp) < datetime.now():
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Token expired",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#     except(jwt.JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     user: Union[dict[str, Any], None] = db.get(token_data.sub, None)
#
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Could not find user",
#         )
#
#     return SystemUser(**user)