# conftest.py
import pytest

@pytest.fixture(scope='session')
def base_url():
    return "https://qa-scooter.praktikum-services.ru"

@pytest.fixture(scope='session')
def endpoints():
    return {
        "create_order": "/api/v1/orders",
        "list_orders": "/api/v1/orders",
    }
