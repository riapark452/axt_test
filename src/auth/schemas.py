from pydantic import BaseModel, Field

from src.app.schemas import UserDetail


class AuthUser(BaseModel):
    username: str
    password: str = Field(min_length=6, max_length=128)


class JWTData(BaseModel):
    user_id: int = Field(alias="sub")
    is_admin: bool = False


class AccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserDetail
