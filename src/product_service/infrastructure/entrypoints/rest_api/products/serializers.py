from pydantic import BaseModel

from domain.models import Product


class ProductsSerializer(BaseModel):
    items: list[Product]
