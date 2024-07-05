from collections.abc import Sequence

from fastapi import APIRouter
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from infrastructure.storage.orm.database import async_session_maker
from infrastructure.storage.orm.models import ProductModel
from .serializers import ProductsSerializer

router = APIRouter(prefix='/products', tags=['products'])


@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=list[ProductsSerializer],
)
async def get_products() -> Sequence[ProductModel]:
    async_session = async_session_maker()
    products = (await async_session.execute(
        select(ProductModel)
        .options(selectinload(ProductModel.currency))
        .options(selectinload(ProductModel.ingredients))
        .options(selectinload(ProductModel.suppliers))
        .options(selectinload(ProductModel.type))
    )).scalars().all()

    return {'items': products}
