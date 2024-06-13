import decimal
from collections.abc import Sequence

from domain.models import Ingredient
from domain.models import Product
from domain.models import ProductType
from domain.models import Supplier


def add_product(
    supplier: Supplier,
    ingredients: Sequence[Ingredient],
    product_type: ProductType,
    name: str,
    price: decimal.Decimal,
) -> Product:
    pass
