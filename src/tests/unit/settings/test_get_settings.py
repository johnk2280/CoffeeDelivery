from config import get_settings
from config import TestConfig


def test_get_settings():
    settings = get_settings()

    assert isinstance(settings, TestConfig)
