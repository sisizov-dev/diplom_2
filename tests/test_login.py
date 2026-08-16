import allure
import pytest
from helpers.api_helpers import login_user, assert_status_code, assert_response_has_key


@allure.epic("Управление пользователями")
@allure.feature("Логин")
class TestLoginUser:

    @allure.story("Вход под существующим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_existing_user(self, api_client, created_user):
        """Тест 1: Вход под существующим пользователем → 200"""
        user_data, token = created_user

        with allure.step("Отправка запроса на логин"):
            response = api_client.post("/api/auth/login", data=user_data)

        with allure.step("Проверка ответа"):
            assert_status_code(response, 200)
            assert_response_has_key(response, "accessToken")
            assert_response_has_key(response, "refreshToken")
            assert response.json()["user"]["email"] == user_data["email"]
            assert response.json()["user"]["name"] == user_data["name"]


    @allure.story("Вход с неверными данными")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_invalid_credentials(self, api_client):
        """Тест 2: Вход с неверным логином и паролем → 401"""
        invalid_user = {
            "email": "fake@mail.com",
            "password": "wrongpass"
        }
        response = api_client.post("/api/auth/login", data=invalid_user)
        
        assert_status_code(response, 401)
        assert response.json()["message"] == "email or password are incorrect"
        