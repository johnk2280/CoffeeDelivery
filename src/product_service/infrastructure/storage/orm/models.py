import decimal

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from .orm_types import BaseModel
from .orm_types import CreatedAt
from .orm_types import CurrencyFK
from .orm_types import ProductTypeFK
from .orm_types import SupplierFK
from .orm_types import Txt
from .orm_types import StrUnique
from .orm_types import UnitPK
from .orm_types import UpdatedAt
from .orm_types import UuidPK


class UnitModel(BaseModel):
    __tablename__ = 'units'

    id: Mapped[UuidPK]
    name: Mapped[StrUnique]


class ProductTypeModel(BaseModel):
    __tablename__ = 'product_types'

    id: Mapped[UuidPK]
    name: Mapped[StrUnique]

    products: Mapped[set['ProductModel']] = relationship(
        secondary='product_types_products',
        back_populates='type',
    )


product_types_products = Table(
    'product_types_products',
    BaseModel.metadata,
    Column('product_type_id', ForeignKey('product_types.id'), primary_key=True),
    Column('product_id', ForeignKey('products.id'), primary_key=True),
)


class IngredientModel(BaseModel):
    __tablename__ = 'ingredients'

    id: Mapped[UuidPK]
    mame: Mapped[StrUnique]

    products: Mapped[list['ProductModel']] = relationship(
        secondary='ingredients_products',
        back_populates='ingredients',
    )


ingredients_products = Table(
    'ingredients_products',
    BaseModel.metadata,
    Column('ingredient_id', ForeignKey('ingredients.id'), primary_key=True),
    Column('product_id', ForeignKey('products.id'), primary_key=True),
)


class SupplierModel(BaseModel):
    __tablename__ = 'suppliers'

    id: Mapped[UuidPK]
    name: Mapped[StrUnique]
    address: Mapped[Txt]

    products: Mapped[list['ProductModel']] = relationship(
        secondary='suppliers_products',
        back_populates='suppliers',
    )
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]


suppliers_products = Table(
    'suppliers_products',
    BaseModel.metadata,
    Column('supplier_id', ForeignKey('suppliers.id'), primary_key=True),
    Column('product_id', ForeignKey('products.id'), primary_key=True),
)


class CurrencyModel(BaseModel):
    __tablename__ = 'currencies'

    id: Mapped[UuidPK]
    name: Mapped[StrUnique]


class ProductModel(BaseModel):
    __tablename__ = 'products'

    id: Mapped[UuidPK]
    name: Mapped[StrUnique]
    price: Mapped[decimal.Decimal]
    currency_id: Mapped[CurrencyFK]
    available: Mapped[bool]
    type_id: Mapped[ProductTypeFK]
    quantity: Mapped[int]
    unit_id: Mapped[UnitPK]
    supplier_id: Mapped[SupplierFK]
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    currency: Mapped['CurrencyModel'] = relationship()
    type: Mapped['ProductTypeModel'] = relationship(
        secondary='product_types_products',
        back_populates='products',
    )
    ingredients: Mapped[set['IngredientModel']] = relationship(
        secondary='ingredients_products',
        back_populates='products',
    )
    suppliers: Mapped[set['SupplierModel']] = relationship(
        secondary='suppliers_products',
        back_populates='products',
    )
