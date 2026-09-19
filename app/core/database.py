from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

database_name = settings.database_url.rsplit("/", maxsplit=1)[-1]

server_url = settings.database_url.rsplit("/", maxsplit=1)[0]

engine = create_async_engine(
    settings.database_url,
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def create_database() -> None:

    server_engine = create_async_engine(
        server_url,
        isolation_level="AUTOCOMMIT",
    )

    try:
        async with server_engine.connect() as connection:
            await connection.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS `{database_name}`"
                )
            )
    finally:
        await server_engine.dispose()

async def get_db() -> AsyncGenerator[AsyncSession, None]:

    async with AsyncSessionLocal() as session:
        yield session