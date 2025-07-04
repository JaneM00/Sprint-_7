# conftest.py
import pytest
import requests
from helpers import generate_courier_data, generate_order_data
from urls import BASE_URL, COURIER_REGISTER

@pytest.fixture(scope='function')
def create_courier():
    data = generate_courier_data()
    response = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
    # Проверка успешного создания или существования курьера
    assert response.status_code in [201, 409]
    return data

@pytest.fixture(scope='function')
def create_order():
    from helpers import generate_order_data
    order_data = generate_order_data()
    response = requests.post(f"{BASE_URL}/v1/orders", json=order_data)
    # Можно добавить проверку успешности создания заказа, если нужно
    assert response.status_code in [200, 201]
    return order_data
