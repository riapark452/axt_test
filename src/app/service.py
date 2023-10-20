from datetime import datetime, date
from typing import List, Dict, Any

from sqlalchemy import insert, select, update, delete, or_, text, asc, desc, and_
from sqlalchemy.dialects.postgresql import Any

from database.connection import fetch_one, execute, fetch_all
from src.app.exceptions import BirthdateNotValid
from src.app.schemas import User, UserUpdate
from src.app.models import user as user_db
from src.auth.security import hash_password


async def create_user(user: User) -> dict[str, Any] | None:
    try:
        insert_query = (
            insert(user_db)
            .values(
                {
                    "username": user.username,
                    "name": user.name,
                    "password": hash_password(user.password),
                    "birthdate": datetime.strptime(user.birthdate, '%Y-%m-%d'),
                    "is_admin": user.is_admin,
                    "is_online": user.is_online,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
            )
        )
    except ValueError:
        raise BirthdateNotValid
    await execute(insert_query)
    return await get_user_by_username(username=user.username)


async def get_user_by_id(id: int) -> dict[str, Any] | None:
    select_query = (select(user_db).where(user_db.c.id == id))
    return await fetch_one(select_query)


async def get_user_by_username(username: str) -> dict[str, Any] | None:
    select_query = select(user_db).where(user_db.c.username == username)
    return await fetch_one(select_query)


async def get_users(skip: 0, limit: 0,
                    search_q: str | None,
                    is_admin: bool | None,
                    is_online: bool | None,
                    birthdate_lt: str | None,
                    birthdate_gte: str | None,
                    sort_c_asc: str | None,
                    sort_c_desc: str | None) -> list[
    dict[str, Any]]:
    select_query = select(user_db).offset(skip).limit(limit)
    if search_q is not None:
        select_query = select_query.filter(
            (user_db.c.username.ilike(f"%{search_q}%") | (user_db.c.name.ilike(f"%{search_q}%"))))
    if is_admin is not None:
        select_query = select_query.filter(user_db.c.is_admin == is_admin)

    if is_online is not None:
        select_query = select_query.filter(user_db.c.is_online == is_online)

    if birthdate_lt is not None and birthdate_gte is not None:
        try:
            select_query = select_query.filter(
                user_db.c.birthdate.between(datetime.strptime(birthdate_gte, '%Y-%m-%d').date(),
                                            datetime.strptime(birthdate_lt, '%Y-%m-%d').date()))
        except ValueError:
            raise BirthdateNotValid
        
    if sort_c_asc is not None:
        select_query = select_query.order_by(text(convert_sort(sort_c_asc, "ASC")))

    if sort_c_desc is not None:
        select_query = select_query.order_by(text(convert_sort(sort_c_desc, "DESC")))
    print(select_query)

    return await fetch_all(select_query)


def convert_sort(sort, type: str):
    """
    # separate string using split('-')
    split_sort = sort.split('-')
    # join to list with ','
    new_sort = ','.join(split_sort)
    """
    split_sort = sort.split('-')
    return ','.join(f"{x} {type}" for x in split_sort)


async def update_user(user: UserUpdate, id: int) -> dict[str, Any]:
    update_query = update(user_db).where(user_db.c.id == id).values(
        {
            "name": user.name,
            "birthdate": datetime.strptime(user.birthdate, '%Y-%m-%d'),
            "is_admin": user.is_admin,
            "is_online": user.is_online,
            "updated_at": datetime.utcnow()
        }
    )
    await execute(update_query)
    return await get_user_by_id(id)


async def delete_user(id: int) -> dict[str, str]:
    user = await get_user_by_id(id)
    if user is not None:
        delete_query = delete(user_db).where(user_db.c.id == id)
        await execute(delete_query)
        return {"msg": "Successful deletion"}
    return {"msg": "Record with this id doesn't exist"}
