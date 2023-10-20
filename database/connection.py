from sqlalchemy import MetaData, dialects, Delete
from sqlalchemy.dialects.postgresql import Any
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import Select, Insert, Update

from src.constants import DB_NAMING_CONVENTION

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///db.sqlite3"
# database = Database(SQLALCHEMY_DATABASE_URL)
# dialect = dialects.sqlite.dialect()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)


async def fetch_one(select_query: Select | Insert | Update) -> dict[str, Any] | None:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        return cursor.mappings().first()


async def fetch_all(select_query: Select | Insert | Update) -> list[dict[str, Any]]:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        return cursor.mappings().all()


async def execute(select_query: Insert | Update | Delete) -> None:
    async with engine.begin() as conn:
        await conn.execute(select_query)
