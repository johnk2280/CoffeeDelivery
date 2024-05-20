import uuid
from typing import Any

from domain import Order
from domain import OrderItem


def place_order(items: list[dict[str, Any]]) -> Order:
    if not items:
        raise ValueError('Items cannot be empty')

    order_id = uuid.uuid4()

    return Order(
        id=order_id,
        items=[OrderItem(
            **el | dict(
                id=uuid.uuid4(),
                order_id=order_id,
            ),
        ) for el in items],
    )
