from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from config import get_settings

settings = get_settings()

DATABASE_PARAMS = dict(
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
)

engine = create_async_engine(settings.database_url, **DATABASE_PARAMS)
async_session_maker = async_sessionmaker[AsyncSession](
    engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
