import json

import allure
import requests
import jsonschema
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        payload: dict [str, ...] = {
            "id": 9999,
            "name": "Non-existent Pet",
            "status": "available"
        }

        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)
        with allure.step("Валидируем ожидаемый код ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"
        with allure.step("Валидация текста в респонсе ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1, "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [
                    {
                        "id": 0, "name": "string"
                    }
                ],
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и JSON schema"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id incorrect"
            assert response_json['name'] == payload['name'], "name incorrect"
            assert response_json['category'] == payload['category'], "category incorrect"
            assert response_json['photoUrls'] == payload['photoUrls'], "photoUrls incorrect"
            assert response_json['tags'] == payload['tags'], "tags incorrect"
            assert response_json['status'] == payload['status'], "status incorrect"