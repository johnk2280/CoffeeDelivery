import datetime
import decimal
import uuid

from domain.models import Currency
from domain.models import Ingredient
from domain.models import Product
from domain.models import ProductType
from domain.models import Supplier
from domain.models import Unit
from service_layer import add_product


def test_add_product():
    unit = Unit(id=uuid.uuid4(), name='шт')
    type_ = ProductType(id=uuid.uuid4(), name='выпечка')
    ingredient_1 = Ingredient(
        id=uuid.uuid4(),
        name='мука пшеничная',
        products=None
    )
    ingredient_2 = Ingredient(id=uuid.uuid4(), name='вода', products=None)
    ingredient_3 = Ingredient(
        id=uuid.uuid4(),
        name='дрожжи хлебопекарные',
        products=None
    )
    supplier = Supplier(
        id=uuid.uuid4(),
        name='ООО Бодрые единороги',
        address='Москва',
        inn=777,
    )
    currency = Currency(id=uuid.uuid4(), name='Руб')
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

    result = add_product(
        supplier=supplier,
        ingredients=[ingredient_1, ingredient_2, ingredient_3],
        product_type=type_,
        name='хлеб пшеничный',
        price=decimal.Decimal('50'),
        currency=currency,
        quantity=10,
        available=True,
        unit=unit,
    )

    assert result.name == 'хлеб пшеничный'
