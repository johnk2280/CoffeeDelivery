from decimal import Decimal

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.storage.orm.models import CurrencyModel
from infrastructure.storage.orm.models import ProductModel
from infrastructure.storage.orm.models import ProductTypeModel
from infrastructure.storage.orm.models import SupplierModel
from infrastructure.storage.orm.models import UnitModel


async def test_create_product(async_session: AsyncSession):
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

    result = (await async_session.execute(select(ProductModel))).scalars().all()

    [p] = result

    assert len(result) == 1
    assert p == product


