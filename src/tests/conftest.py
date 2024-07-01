import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from config import get_settings
from config import Settings
from infrastructure.storage.orm.orm_types import BaseModel


@pytest_asyncio.fixture(scope='session', autouse=True)
def event_loop(request):  # noqa: ARG001
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope='session')
def async_engine(settings: Settings) -> AsyncEngine:
    assert settings.ENVIRONMENT.lower() == 'test'

    return create_async_engine(settings.database_url, poolclass=NullPool)


@pytest.fixture(scope='session', autouse=True)
async def async_db_engine(
    async_engine: AsyncEngine,
) -> AsyncGenerator[AsyncEngine, None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest.fixture(scope='function', autouse=True)
async def async_session(
    async_db_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker[AsyncSession](
        async_db_engine,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session
