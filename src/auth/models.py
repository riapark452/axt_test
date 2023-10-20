from sqlalchemy import Table, Column, ForeignKey, String, DateTime, func, MetaData, Integer, Identity

from src.app.models import user
from src.constants import DB_NAMING_CONVENTION

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

refresh_tokens = Table(
    "auth_refresh_token",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("user_id",Integer, ForeignKey(user.c.id, ondelete="CASCADE"), nullable=False),
    Column("refresh_token", String, nullable=False),
    Column("expires_at", DateTime, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)


# async def init_refresh_token_model():
#     await database.connect()
#     for table in metadata.tables.values():
#         schema = sqlalchemy.schema.CreateTable(table, if_not_exists=True)
#         query = str(schema.compile(dialect=dialect))
#         await database.execute(query=query)
#     await database.disconnect()
