import allure
import pytest
import requests
import jsonschema
from .schemas.inventory_schema import INVENTORY_SCHEMA
from .schemas.order_schema import ORDER_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа (POST /store/order)")
    def test_post_store_order(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Валидация JSON Schema"):
            jsonschema.validate(response_json, ORDER_SCHEMA)

    @allure.title("Получение информации о заказе по ID (GET /store/order/{orderId})")
    def test_get_store_order(self, create_store_order):
        order_id = create_store_order['id']
        with allure.step(f"Отправка GET-запроса на получение информации о заказе {order_id}"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            response_json = response.json()
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response_json['id'] == order_id, "id incorrect"

    @allure.title("Удаление заказа по ID (DELETE /store/order/{orderId})")
    def test_delete_store_order(self, create_store_order):
        order_id = create_store_order['id']
        with allure.step(f"Отправка DELETE-запроса на удаление информации о заказе {order_id}"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step(f"Отправка GET-запроса на получение информации о заказе {order_id}"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе (GET /store/order/{orderId})")
    def test_get_nonexistent_store_order(self):
        nonexistent_store_order = 9999
        with allure.step(f"Отправка GET-запроса на получение информации о несуществующем заказе {nonexistent_store_order}"):
            response = requests.get(url=f"{BASE_URL}/store/order/{nonexistent_store_order}")
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина (GET /store/inventory)")
    def test_get_store_inventory(self):
        with allure.step("Отправка GET-запроса на получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            response_json = response.json()

        with allure.step("Валидация JSON Schema"):
            jsonschema.validate(response_json, INVENTORY_SCHEMA)