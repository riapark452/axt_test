from sqlalchemy import Column, String, Integer, DateTime, Boolean, Table, \
    Identity, LargeBinary, func, Date

from database.connection import metadata

user = Table(
    "user",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("username", String, nullable=False),
    Column("name", String, nullable=False),
    Column("password", LargeBinary, nullable=False),
    Column("birthdate", Date, nullable=False),
    Column("is_admin", Boolean, server_default="false", nullable=False),
    Column("is_online", Boolean, server_default="false", nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)
