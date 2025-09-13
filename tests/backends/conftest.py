import pytest
from httpx import AsyncClient
from main import app
from unittest.mock import AsyncMock, patch

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

# Мок для Redis
@pytest.fixture
def mock_redis():
    with patch("crud.redis.get_user_by_token", new_callable=AsyncMock) as mock:
        yield mock

# Мок для PostgreSQL refresh token
@pytest.fixture
def mock_postgres_refresh():
    with patch("crud.sqlmodel.get_user_id_by_refresh_token", new_callable=AsyncMock) as mock:
        yield mock

# Мок для MongoDB
@pytest.fixture
def mock_mongo():
    with patch("crud.motor.create_message", new_callable=AsyncMock) as mock_create, \
         patch("crud.motor.get_user_messages", new_callable=AsyncMock) as mock_get:
        yield mock_create, mock_get

# Мок для NLP
@pytest.fixture
def mock_nlp():
    with patch("nlp.pipeline.nlp_pipeline", new_callable=AsyncMock) as mock:
        yield mock
