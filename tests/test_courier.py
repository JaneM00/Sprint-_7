# test_courier.py
import requests
import pytest
import allure
from urls import BASE_URL, COURIER_REGISTER, COURIER_LOGIN

def generate_random_string(length=10) -> str:
    import string, random
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

@pytest.fixture
def create_courier() -> dict:
    # Генерируем уникальные данные для курьера
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()
    data = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    # Создаем курьера
    response = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
    # Проверяем успешное создание или существование (код 409)
    assert response.status_code in [201, 409]
    return data

class TestCourier:
    def generate_courier_data(self) -> dict:
        login = generate_random_string()
        password = generate_random_string()
        first_name = generate_random_string()
        return {
            "login": login,
            "password": password,
            "firstName": first_name
        }

    @allure.title("Успешная регистрация курьера")
    def test_register_courier(self):
        data = self.generate_courier_data()
        response = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Регистрация дублирующегося курьера")
    def test_create_duplicate_courier(self):
        data = self.generate_courier_data()
        resp1 = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
        assert resp1.status_code in [201, 409]

        # Попытка создать такого же курьера еще раз
        resp2 = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
        # Ожидаем ошибку (например, 409 Conflict)
        assert resp2.status_code != 201

    @allure.title("Регистрация курьера с пропущенными полями")
    def test_create_courier_missing_fields(self):
        base_data = self.generate_courier_data()
        for field in ["login", "password", "firstName"]:
            data = base_data.copy()
            del data[field]
            response = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
            # Ожидаем ошибку (например, 400 Bad Request)
            assert response.status_code != 201

    @allure.title("Авторизация курьера успешно")
    def test_authorize_success(self, create_courier: dict):
        response = requests.post(f"{BASE_URL}{COURIER_LOGIN}", json={
            "login": create_courier["login"],
            "password": create_courier["password"]
        })
        assert response.status_code == 200
        resp_json = response.json()
        # Проверка наличия id или токена в ответе
        assert isinstance(resp_json.get("id"), int) or ("token" in resp_json)

    @allure.title("Авторизация с неправильными данными")
    def test_authorize_wrong_credentials(self, create_courier: dict):
        response = requests.post(f"{BASE_URL}{COURIER_LOGIN}", json={
            "login": create_courier["login"],
            "password": create_courier["password"] + "_wrong"
        })
        # Ожидаем ошибку авторизации (например, не 200)
        assert response.status_code != 200

    @allure.title("Авторизация без обязательных полей")
    def test_authorize_missing_fields(self, create_courier: dict):
       for field in ["login", "password"]:
           data = {
               "login": create_courier["login"],
               "password": create_courier["password"]
           }
           del data[field]
           response = requests.post(f"{BASE_URL}{COURIER_LOGIN}", json=data)
           # Ожидаем ошибку (например, 400 Bad Request)
           assert response.status_code != 200
