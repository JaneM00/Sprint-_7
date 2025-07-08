# conftest.py
import pytest

@pytest.fixture(scope='session')
def base_url():
    return "https://qa-scooter.praktikum-services.ru"

@pytest.fixture(scope='session')
def endpoints():
    return {
        "create_order": "/v1/orders",
        "list_orders": "/v1/orders",
        "register_courier": "/v1/courier",
        "login_courier": "/v1/courier/login",
    }
