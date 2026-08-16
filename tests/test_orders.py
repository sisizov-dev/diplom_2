import allure
import pytest
from helpers.api_helpers import create_order, get_ingredients, assert_status_code, assert_response_has_key


@allure.epic("Заказы")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.story("Создание заказа с авторизацией")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_auth(self, api_client, created_user):
        """Тест 1: Создание заказа с авторизацией → 200"""
        user_data, token = created_user
        ingredients = {"ingredients": ["61c0c5a71d1f82001bdaaa6d"]}

        with allure.step("Отправка запроса на создание заказа"):
            response = create_order(ingredients, token)

        with allure.step("Проверка ответа"):
            assert_status_code(response, 200)
            assert_response_has_key(response, "order")
            assert response.json()["success"] is True

    @allure.story("Создание заказа без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_auth(self, api_client):
        ingredients = {"ingredients": ["61c0c5a71d1f82001bdaaa6d"]}
        response = create_order(ingredients)

        assert_status_code(response, 200)
        assert response.json()["success"] is True

    @allure.story("Создание заказа с ингредиентами")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_ingredients(self, api_client):
        ingredients = {"ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]}
        response = create_order(ingredients)
        
        assert_status_code(response, 200)
        assert_response_has_key(response, "order")

    @allure.story("Создание заказа без ингредиентов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_ingredients(self, api_client):
        ingredients = {"ingredients": []}
        response = create_order(ingredients)
        
        assert_status_code(response, 400)
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.story("Создание заказа с неверным хешем ингредиентов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_invalid_hash(self, api_client):
    # Получаем реальный ID ингредиента
        ingredients_response = get_ingredients()
        real_id = ingredients_response.json()["data"][0]["_id"]
    
    # Меняем последний символ, чтобы получить несуществующий ID
        invalid_id = real_id[:-1] + "0"  # например, ...6d → ...60
    
        ingredients = {"ingredients": [invalid_id]}
        response = create_order(ingredients)
    
        assert_status_code(response, 500)
        