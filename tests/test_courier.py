# test_courier.py
import requests
import pytest
import allure
from urls import BASE_URL, COURIER_REGISTER, COURIER_LOGIN
from helpers import generate_courier_data

class TestCourier:
    def generate_courier_data(self) -> dict:
        return generate_courier_data()

    @allure.title("Регистрация курьера с пропущенными обязательными полями")
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_register_missing_field(self, missing_field):
        data = self.generate_courier_data()
        del data[missing_field]
        response = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
        # Проверка статуса и тела ответа
        assert response.status_code == 400
        resp_json = response.json()
        # Проверяем наличие сообщения об ошибке
        assert "message" in resp_json or "error" in resp_json

    @allure.title("Авторизация с неправильными данными возвращает ошибку")
    @pytest.mark.parametrize("wrong_password", [
        ("password_wrong"),
        ("incorrect_password"),
        ("123456")
    ])
    def test_authorize_wrong_passwords(self, wrong_password):
        data = self.generate_courier_data()
        # Регистрация курьера перед тестом авторизации
        register_response = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
        assert register_response.status_code == 201

        login_data = {
            "login": data["login"],
            "password": wrong_password
        }
        
        response = requests.post(f"{BASE_URL}{COURIER_LOGIN}", json=login_data)
        
        # Проверка статуса и тела ошибки (ожидаем ошибку)
        assert response.status_code != 200
        resp_json = response.json()
        assert "message" in resp_json or "error" in resp_json

    @allure.title("Авторизация без обязательных полей возвращает ошибку")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_authorize_missing_fields(self, missing_field):
        data = self.generate_courier_data()

        login_data = {
            "login": data["login"],
            "password": data["password"]
        }
        
        del login_data[missing_field]
        
        # Перед авторизацией регистрируем курьера для корректности теста
        register_response = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
        assert register_response.status_code == 201

        response = requests.post(f"{BASE_URL}{COURIER_LOGIN}", json=login_data)

        # Проверка статуса и тела ошибки (ожидаем ошибку)
        assert response.status_code != 200
      	resp_json = response.json()
      	# Проверяем наличие сообщения об ошибке в теле ответа
      	assert "message" in resp_json or "error" in resp_json
