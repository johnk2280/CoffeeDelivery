import uuid
from contextlib import nullcontext
from typing import Any

import pytest

from domain import Order
from service_layer import place_order


@pytest.mark.parametrize(
    'items, expected, expectation', [
        ([{}], None, pytest.raises(TypeError)),
        ([], None, pytest.raises(ValueError)),
        (
                [
                    {
                        'product': 'capuccino',
                        'size': 'medium',
                        'quantity': 1,
                    },
                ],
                Order(id=uuid.uuid4(), items=[]),
                nullcontext(),
        )
    ]
)
def test_place_order(
    items: list[dict[str, Any]],
    expected: Order,
    expectation: Any,
) -> None:

    with expectation:
        assert place_order(items) == expected
