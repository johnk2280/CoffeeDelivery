import uuid
from typing import Any

from domain import Order
from domain import OrderItem


def place_order(items: list[dict[str, Any]]) -> Order:
    if not items:
        raise ValueError('Items cannot be empty')

    return Order(
        id=uuid.uuid4(),
        items=[OrderItem(**el) for el in items],
    )
