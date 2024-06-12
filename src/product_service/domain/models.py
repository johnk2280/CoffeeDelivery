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


class Supplier(BaseModel):
    id: uuid.UUID
    name: str
    address: str
    inn: str


class Product(BaseModel):
    id: uuid.UUID
    name: str
    price: decimal
    available: bool
    type: ProductType
    ingredients: set[Ingredient]
    supplier: Supplier
    created_at: datetime.datetime
    updated_at: datetime.datetime

