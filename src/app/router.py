import json
from datetime import datetime
from typing import List, Dict, Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy import insert
from starlette import status
from starlette.responses import JSONResponse

from database.connection import execute
from src.app import service
from src.app.dependencies import valid_user_create
from src.app.models import user
from src.app.schemas import User, UserDetail, UserUpdate
from src.auth.jwt import oauth2_scheme, parse_jwt_user_data
from src.auth.security import hash_password

router = APIRouter()


@router.get("/list/all", status_code=status.HTTP_200_OK, response_model=List[UserDetail])
async def get_users(skip: int = 0, limit: int = 10, search_q: str | None = Query(default=None, max_length=50),
                    is_admin: bool | None = Query(default=None),
                    is_online: bool | None = Query(default=None),
                    birthdate_lt: str | None = Query(default=None),
                    birthdate_gte: str | None = Query(default=None),
                    sort_c_asc: str | None = Query(default=None, max_length=50),
                    sort_c_desc: str | None = Query(default=None, max_length=50),
                    token: str = Depends(parse_jwt_user_data)) -> list[dict[str, Any]]:
    users = await service.get_users(skip, limit, search_q, is_admin, is_online, birthdate_lt, birthdate_gte, sort_c_asc,
                                    sort_c_desc)
    return users


@router.get("/get/{id}", status_code=status.HTTP_200_OK, response_model=UserDetail)
async def get_user(id: int, token: str = Depends(parse_jwt_user_data)) -> dict[str, Any] | JSONResponse:
    user = await service.get_user_by_id(id)
    if user is not None:
        return user
    else:
        return JSONResponse({"msg": "User not found"}, status_code=status.HTTP_404_NOT_FOUND)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserDetail)
async def add_user(data: User = Depends(valid_user_create)) -> dict[
    str, str]:
    user = await service.create_user(data)
    return user


@router.put("/update/{id}", status_code=status.HTTP_200_OK, response_model=UserDetail)
async def update_user(id: int, data: UserUpdate,
                      token: str = Depends(parse_jwt_user_data)) -> dict[str, Any] | JSONResponse:
    user = await service.update_user(data, id)
    if user is not None:
        return user
    else:
        return JSONResponse({"msg": "User not found"}, status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: int, token: str = Depends(parse_jwt_user_data)) -> dict[str, str]:
    response = await service.delete_user(id)
    return response
