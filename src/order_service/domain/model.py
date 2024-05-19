import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderItem:
    id: uuid.UUID
    order_id: uuid.UUID
    product: str
    size: int
    quantity: int
