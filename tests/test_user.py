import allure
import pytest
from helpers.api_helpers import assert_status_code, assert_response_has_key


@allure.epic("Управление пользователями")
@allure.feature("Регистрация")
class TestCreateUser:

    @allure.story("Создание уникального пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_unique_user(self, api_client, created_user):
        """Тест 1: Создание уникального пользователя → 200"""
        user_data, token = created_user
    
        with allure.step("Проверка, что пользователь создан"):
            assert token is not None
            assert user_data["email"] is not None
            assert user_data["name"] is not None

    @allure.story("Создание уже существующего пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_existing_user(self, api_client, created_user):
        """Тест 2: Создание уже зарегистрированного пользователя → 403"""
        user_data, token = created_user
        with allure.step("Создание пользователя"):
            api_client.post("/api/auth/register", data=user_data)

        with allure.step("Повторная попытка регистрации"):
            response = api_client.post("/api/auth/register", data=user_data)

        with allure.step("Проверка ответа"):
            assert_status_code(response, 403)
            assert response.json()["message"] == "User already exists"

    @allure.story("Создание пользователя без обязательного поля")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("field_to_remove", [
        "email",
        "password",
        "name"
    ])
    def test_create_user_without_field(self, api_client, test_user, field_to_remove):
        """Тест 3: Создание пользователя без обязательного поля → 403"""
        with allure.step(f"Удаление поля '{field_to_remove}' из данных"):
            incomplete_user = test_user.copy()
            del incomplete_user[field_to_remove]

        with allure.step("Отправка запроса на регистрацию"):
            response = api_client.post("/api/auth/register", data=incomplete_user)

        with allure.step("Проверка ответа"):
            assert_status_code(response, 403)
            