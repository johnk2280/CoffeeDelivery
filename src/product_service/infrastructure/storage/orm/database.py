from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_PARAMS = dict(
    pool_size=10,
    max_overflow=10,
)

engine = create_async_engine(**DATABASE_PARAMS)
