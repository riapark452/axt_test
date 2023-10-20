import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field()
    name: str = Field()
    password: str = Field(min_length=6, max_length=128)
    birthdate: str = Field()
    is_admin: bool = Field()
    is_online: bool = Field()

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "name": "John Doe",
                "password": "weakpassword"
            }
        }


class UserDetail(BaseModel):
    id: int
    username: str = Field()
    name: str = Field()
    birthdate: datetime.date = Field()
    is_admin: bool = Field()
    is_online: bool = Field()
    created_at: datetime.datetime
    updated_at: datetime.datetime = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "name": "John Doe",
                "password": "weakpassword"
            }
        }


class UserUpdate(BaseModel):
    name: str = Field()
    birthdate: str = Field()
    is_admin: bool = Field()
    is_online: bool = Field()

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "name": "John Doe",
                "password": "weakpassword"
            }
        }


class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "weakpassword"
            }
        }
