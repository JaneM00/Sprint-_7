# test_courier.py
import requests
import pytest
from urls import BASE_URL, COURIER_REGISTER, COURIER_LOGIN

class TestCourier:
    def courier_credentials(self):
        return {
            "login": "testuser",
            "password": "testpass"
        }

    def test_register_courier(self):
        data = self.courier_credentials()
        response = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
        assert response.status_code in [200, 201]
        
    def test_login_courier(self):
        data = self.courier_credentials()
        response = requests.post(f"{BASE_URL}{COURIER_LOGIN}", json=data)
        assert response.status_code == 200
        resp_json = response.json()
        
        # Проверка наличия токена или другого ключа авторизации.
        assert "accessToken" in resp_json or "token" in resp_json
