# conftest.py
import pytest
import requests
from urls import BASE_URL, COURIER_REGISTER, COURIER_LOGIN

@pytest.fixture(scope='session')
def courier_token():
    # Регистрация курьера (если нужно)
    credentials = {
        "login": "testuser",
        "password": "testpass"
    }
    # Попытка зарегистрировать (может быть уже зарегистрирован)
    requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=credentials)

    # Логин и получение токена
    response = requests.post(f"{BASE_URL}{COURIER_LOGIN}", json=credentials)
    response.raise_for_status()
    token_response = response.json()
    token = token_response.get("accessToken") or token_response.get("token")
    
    return token

@pytest.fixture
def authorized_headers(courier_token):
    return {
        "Authorization": f"Bearer {courier_token}"
    }
