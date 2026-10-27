from fastapi import Request
from app.core.config import config
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy import URL

conn_url = URL.create(
    drivername=config.database_drivername,
    username=config.database_user,
    password=config.database_password,
    host=config.database_host,
    database=config.database_name,
    port=config.database_port,
)


async_engine = create_async_engine(
    url=conn_url, poolclass=AsyncAdaptedQueuePool, pool_size=3, max_overflow=10
)

AsyncSessionContext = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def get_db_connection() -> AsyncGenerator[AsyncSession, None]:

    async with AsyncSessionContext() as session:
        yield session
