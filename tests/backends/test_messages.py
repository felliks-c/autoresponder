import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_send_message_success(async_client: AsyncClient, mock_redis, mock_postgres_refresh, mock_mongo, mock_nlp):
    mock_redis.return_value = "1"           # access token найден
    mock_postgres_refresh.return_value = None
    mock_create, mock_get = mock_mongo
    mock_nlp.return_value = ("Ответ", "тип")

    response = await async_client.post(
        "/messages/send",
        headers={"Authorization": "Bearer valid_token"},
        json={"text": "Привет"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] == "Ответ"
    mock_create.assert_called_once()

@pytest.mark.asyncio
async def test_send_message_unauthorized(async_client: AsyncClient, mock_redis, mock_postgres_refresh):
    mock_redis.return_value = None
    mock_postgres_refresh.return_value = None

    response = await async_client.post(
        "/messages/send",
        headers={"Authorization": "Bearer invalid_token"},
        json={"text": "Привет"}
    )
    assert response.status_code == 401
