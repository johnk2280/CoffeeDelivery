import asyncio
from collections.abc import AsyncGenerator
from decimal import Decimal
from typing import TypedDict

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy import NullPool
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from config import get_settings
from config import Settings
from infrastructure.entrypoints.rest_api.app import create_app
from infrastructure.entrypoints.rest_api.products import product_router
from infrastructure.storage.orm.models import CurrencyModel
from infrastructure.storage.orm.models import ProductModel
from infrastructure.storage.orm.models import ProductTypeModel
from infrastructure.storage.orm.models import SupplierModel
from infrastructure.storage.orm.models import UnitModel
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


@pytest.fixture(scope='function')
async def async_client(
    settings: Settings,
) -> AsyncGenerator[AsyncClient, None]:
    app = create_app(settings, [product_router])

    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


class PrepDataYieldType(TypedDict):
    unit: UnitModel
    type: ProductTypeModel
    supplier: SupplierModel
    currency: CurrencyModel
    product: ProductModel


@pytest.fixture(scope='function')
async def prep_data(
    async_session: AsyncSession,
) -> AsyncGenerator[PrepDataYieldType, None]:

    for table in BaseModel.metadata.sorted_tables:
        await async_session.execute(
            text(f'TRUNCATE {table.name} CASCADE;'),
        )
        await async_session.commit()

    unit = (await async_session.execute(
        insert(UnitModel)
        .values(name='Порция')
        .returning(UnitModel),
    )).scalars().one()

    type_ = (await async_session.execute(
        insert(ProductTypeModel)
        .values(name='Гарнир')
        .returning(ProductTypeModel),
    )).scalars().one()

    supplier = (await async_session.execute(
        insert(SupplierModel)
        .values(
            name='Розовый пони',
            address='г.Москва',
        )
        .returning(SupplierModel),
    )).scalars().one()

    currency = (await async_session.execute(
        insert(CurrencyModel)
        .values(name='Руб.')
        .returning(CurrencyModel),
    )).scalars().one()

    product = (await async_session.execute(
        insert(ProductModel)
        .values(
            name='Каша гречневая на воде',
            price=Decimal('35.50'),
            currency_id=currency.id,
            available=True,
            type_id=type_.id,
            quantity=5,
            unit_id=unit.id,
            supplier_id=supplier.id,
        )
        .returning(ProductModel),
    )).scalars().one()

    await async_session.commit()
    # await async_session.close()

    yield {
        'unit': unit,
        'type': type_,
        'supplier': supplier,
        'currency': currency,
        'product': product,
    }

    for table in BaseModel.metadata.sorted_tables:
        await async_session.execute(
            text(f'TRUNCATE {table.name} CASCADE;'),
        )
        await async_session.commit()
