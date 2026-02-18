import json
from http.client import responses

import allure
import pytest
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

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "Buddy",
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
            assert response_json['status'] == payload['status'], "status incorrect"

    @allure.title("Добавление нового питомца с полными данными")
    def test_add_pet_with_full_details(self):
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

    @allure.title("Получение информации о питомце по ID (GET /pet{petId})")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet['id']

        with allure.step("Отправка запроса (GET /pet{petId})"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            response_json = response.json()

        with allure.step("Проверка status code ответа и валидация pet_id"):
            assert response.status_code == 200, "status code incorrect"
            assert response_json['id'] == pet_id, "pet_id incorrect"

    @allure.title("Обновление информации о питомце (PUT /pet)")
    def test_update_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet['id']

        with allure.step("Подготовка данных для обновления"):
            payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка PUT /pet{petId} с подготовленными данными"):
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()
            assert response.status_code == 200, "status code incorrect"
            assert response_json['id'] == pet_id, "pet_id incorrect"
            assert response_json['name'] == payload['name'], "name incorrect"
            assert response_json['status'] == payload['status'], "status incorrect"

    @allure.title("Удаление питомца по ID (DELETE /pet/{petId})")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet['id']

        with allure.step("Отправка DELETE /pet{petId} созданного питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 200, "status code incorrect"

        with allure.step("Отправка GET /pet{petId} удаленного питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 404, "status code incorrect"

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        'status, expected_status_code',
        [
            ('available', 200),
            ('pending', 200),
            ('sold', 200),
            ('jerk', 400),
            ('', 400)
        ]
    )
    def test_get_pets_by_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомцев по статусу {status}"):
            response = requests.get(url=f"{BASE_URL}/pet/findByStatus", params={"status": status})
            assert response.status_code == expected_status_code, "status code incorrect"
            if response.status_code == 200:
                assert isinstance(response.json(), list), "response data type incorrect"