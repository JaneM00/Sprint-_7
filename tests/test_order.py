# test_order.py
import requests
import pytest
import allure
from locators import BASE_URL, ORDERS_CREATE, ORDERS_LIST
from data import get_sample_order_data

class TestOrder:
    @pytest.mark.parametrize("colors", [
        [],
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"]
    ])
    @allure.title("Создание заказа с цветами: {colors}")
    def test_create_order_with_colors(self, colors):
        order_body = get_sample_order_data()
        order_body['color'] = colors

        # Удаляем ключи со значением пустого списка или None, если нужно
        order_body_cleaned = {k: v for k, v in order_body.items() if v not in [None, [], ""]}

        with allure.step("Отправка POST-запрос на создание заказа"):
            response = requests.post(f"{BASE_URL}{ORDERS_CREATE}", json=order_body_cleaned)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code in [200, 201], f"Unexpected status code: {response.status_code}"
        with allure.step("Проверка наличия 'track' в ответе и его типа"):
            resp_json = response.json()
            assert "track" in resp_json, "Response JSON does not contain 'track'"
            assert isinstance(resp_json["track"], int), f"'track' is not an int: {resp_json['track']}"

    @allure.title("Получение списка заказов")
    def test_get_orders(self):
        with allure.step("Отправка GET-запрос на получение списка заказов"):
            response = requests.get(f"{BASE_URL}{ORDERS_LIST}")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        with allure.step("Проверка типа возвращаемого объекта (список)"):
            orders_list = response.json()
            assert isinstance(orders_list, list)
