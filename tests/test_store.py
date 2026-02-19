import allure
import pytest
import requests
import jsonschema
from .schemas.pet_schema import PET_SCHEMA

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
            assert response_json['id'] == payload['id'], "id incorrect"
            assert response_json['petId'] == payload['petId'], "petId incorrect"
            assert response_json['quantity'] == payload['quantity'], "quantity incorrect"
            assert response_json['status'] == payload['status'], "status incorrect"
            assert response_json['complete'] == payload['complete'], "complete incorrect"

    @allure.title("Получение информации о заказе по ID (GET /store/order/{orderId})")
    def test_get_store_order(self, create_store_order):
        pass

    @allure.title("Удаление заказа по ID (DELETE /store/order/{orderId})")
    def test_delete_store_order(self, create_store_order):
        pass

    @allure.title("Попытка получить информацию о несуществующем заказе (GET /store/order/{orderId})")
    def test_get_store_order(self):
        pass

    @allure.title("Получение инвентаря магазина (GET /store/inventory)")
    def test_get_store_inventory(self):
        pass