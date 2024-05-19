import uuid
from dataclasses import dataclass
from enum import Enum


class StatusChoice(str, Enum):
    CREATED = 'created'
    PAID = 'paid'
    PROGRESS = 'progress'
    CANCELLED = 'cancelled'
    DISPATCHED = 'dispatched'
    DELIVERED = 'delivered'


@dataclass(frozen=True)
class OrderItem:
    id: uuid.UUID
    order_id: uuid.UUID
    product: str
    size: int
    quantity: int


@dataclass(frozen=True)
class Order:
    id: uuid.UUID
    items: list[OrderItem]
    status: StatusChoice
