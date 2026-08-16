import pytest
import requests
from helpers.generators import generate_user
from helpers.api_helpers import delete_user


BASE_URL = "https://stellarburgers.education-services.ru"


@pytest.fixture
def test_user():
    return generate_user()


@pytest.fixture
def api_client():
    class APIClient:
        def post(self, endpoint, data=None):
            url = f"{BASE_URL}{endpoint}"
            return requests.post(url, json=data)
    return APIClient()

@pytest.fixture
def created_user(api_client):
    """Фикстура: создаёт пользователя и удаляет его после теста"""
    from helpers.generators import generate_user
    from helpers.api_helpers import delete_user
    
    user_data = generate_user()
    response = api_client.post("/api/auth/register", data=user_data)
    token = response.json().get("accessToken")
    
    yield user_data, token
    
    # Удаляем пользователя после теста
    if token:
        delete_user(token)