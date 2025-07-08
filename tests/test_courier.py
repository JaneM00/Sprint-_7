# test_courier.py
import requests
import pytest
import allure
from urls import BASE_URL, COURIER_REGISTER, COURIER_LOGIN
from helpers import generate_courier_data

class TestCourier:
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    @allure.title("Регистрация курьера с пропущенными обязательными полями")
    def test_register_missing_field(self, missing_field):
        data = generate_courier_data()
        del data[missing_field]
        with allure.step(f"Отправка POST-запрос на регистрацию курьера без поля {missing_field}"):
            response = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
        # Атомарная проверка статуса и тела ответа
        with allure.step("Проверка, что статус код равен 400 (ошибка)"):
            assert response.status_code == 400
        resp_json = response.json()
        with allure.step("Проверка наличия сообщения об ошибке в ответе"):
            assert "message" in resp_json or "error" in resp_json

    @pytest.mark.parametrize("wrong_password", [
        "password_wrong",
        "incorrect_password",
        "123456"
    ])
    @allure.title("Авторизация с неправильными данными возвращает ошибку")
    def test_authorize_wrong_passwords(self, wrong_password):
        data = generate_courier_data()
        # Регистрация курьера перед тестом авторизации
        with allure.step("Регистрация курьера перед тестом авторизации"):
            register_response = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
            with allure.step("Проверка успешной регистрации (статус 201)"):
                assert register_response.status_code == 201

        login_data = {
            "login": data["login"],
            "password": wrong_password
        }
        with allure.step("Отправка POST-запрос на авторизацию с неправильным паролем"):
            response = requests.post(f"{BASE_URL}{COURIER_LOGIN}", json=login_data)
        # Атомарная проверка статуса и тела ответа
        with allure.step("Проверка, что статус код не равен 200 (ошибка)"):
            assert response.status_code != 200
        resp_json = response.json()
        with allure.step("Проверка наличия сообщения об ошибке в ответе"):
            assert "message" in resp_json or "error" in resp_json

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title("Авторизация без обязательных полей возвращает ошибку")
    def test_authorize_missing_fields(self, missing_field):
        data = generate_courier_data()

        login_data = {
            "login": data["login"],
            "password": data["password"]
        }
        
        del login_data[missing_field]
        
        # Перед авторизацией регистрируем курьера для корректности теста
        with allure.step("Регистрация курьера перед тестом авторизации без поля {}".format(missing_field)):
            register_response = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
            with allure.step("Проверка успешной регистрации (статус 201)"):
                assert register_response.status_code == 201

        with allure.step(f"Отправка POST-запрос на авторизацию без поля {missing_field}"):
            response = requests.post(f"{BASE_URL}{COURIER_LOGIN}", json=login_data)
        
        # Атомарная проверка статуса и тела ответа
        with allure.step("Проверка, что статус код не равен 200 (ошибка)"):
            assert response.status_code != 200
        resp_json = response.json()
        with allure.step("Проверка наличия сообщения об ошибке в ответе"):
            assert "message" in resp_json or "error" in resp_json
