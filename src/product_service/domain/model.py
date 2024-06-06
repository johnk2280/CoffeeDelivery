import datetime
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class StatusChoice(str, Enum):
    CREATED = 'created'
    PAID = 'paid'
    PROGRESS = 'progress'
    CANCELLED = 'cancelled'
    DISPATCHED = 'dispatched'
    DELIVERED = 'delivered'


class SizeChoice(str, Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'


@dataclass
class OrderItem:
    id: uuid.UUID
    order_id: uuid.UUID
    product: str
    size: SizeChoice
    quantity: int


@dataclass
class Order:
    id: uuid.UUID
    items: Iterable[OrderItem]
    schedule_id: uuid.UUID | None = None
    delivery_id: uuid.UUID | None = None
    status: StatusChoice = StatusChoice.CREATED
    created_at: datetime.datetime = datetime.datetime.now(datetime.UTC)
    updated_at: datetime.datetime = datetime.datetime.now(datetime.UTC)
