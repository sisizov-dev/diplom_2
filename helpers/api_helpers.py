import allure
import requests

BASE_URL = "https://stellarburgers.education-services.ru/api"


def assert_status_code(response, expected_code):
    """Проверка статус-кода"""
    assert response.status_code == expected_code, \
        f"Ожидался статус {expected_code}, получен {response.status_code}"


def assert_response_has_key(response, key):
    """Проверка наличия ключа в ответе"""
    assert key in response.json(), f"В ответе отсутствует ключ '{key}'"


@allure.step("Отправляем запрос на создание пользователя")
def create_user(payload):
    return requests.post(f"{BASE_URL}/auth/register", json=payload)


@allure.step("Отправляем запрос на логин пользователя")
def login_user(payload):
    return requests.post(f"{BASE_URL}/auth/login", json=payload)


@allure.step("Отправляем запрос на удаление пользователя")
def delete_user(token):
    headers = {"Authorization": token}
    return requests.delete(f"{BASE_URL}/auth/user", headers=headers)


@allure.step("Отправляем запрос на создание заказа")
def create_order(payload, token=None):
    headers = {"Authorization": token} if token else {}
    return requests.post(f"{BASE_URL}/orders", json=payload, headers=headers)


@allure.step("Отправляем запрос на получение списка ингредиентов")
def get_ingredients():
    return requests.get(f"{BASE_URL}/ingredients")