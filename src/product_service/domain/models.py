import datetime
import decimal
import uuid

from pydantic import BaseModel


class Unit(BaseModel):
    id: uuid.UUID
    name: str


class ProductType(BaseModel):
    id: uuid.UUID
    name: str


class Ingredient(BaseModel):
    id: uuid.UUID
    name: str
    products: set['Product'] | None


class Supplier(BaseModel):
    id: uuid.UUID
    name: str
    address: str
    inn: int


class Currency(BaseModel):
    id: uuid.UUID
    name: str


class Product(BaseModel):
    id: uuid.UUID
    name: str
    price: decimal.Decimal
    currency: Currency
    available: bool
    type: ProductType
    ingredients: set[Ingredient]
    quantity: int
    unit: Unit
    supplier: Supplier
    created_at: datetime.datetime
    updated_at: datetime.datetime
