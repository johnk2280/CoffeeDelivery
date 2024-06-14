import decimal
from collections.abc import Sequence

from domain.models import Currency
from domain.models import Ingredient
from domain.models import Product
from domain.models import ProductType
from domain.models import Supplier
from domain.models import Unit


def add_product(
    supplier: Supplier,
    ingredients: Sequence[Ingredient],
    product_type: ProductType,
    name: str,
    price: decimal.Decimal,
    currency: Currency,
    quantity: int,
    available: bool,
    unit: Unit,
) -> Product:
    # product = Product(
    #     id=uuid.uuid4(),
    #     name='хлеб пшеничный',
    #     price=decimal.Decimal('50'),
    #     available=True,
    #     type=type_,
    #     ingredients={ingredient_1, ingredient_2, ingredient_3},
    #     supplier=supplier,
    #     quantity=10,
    #     unit=unit,
    #     created_at=datetime.datetime.now(datetime.UTC),
    #     updated_at=datetime.datetime.now(datetime.UTC),
    # )

    pass
