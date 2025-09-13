import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_history_success(async_client: AsyncClient, mock_mongo):
    mock_create, mock_get = mock_mongo
    mock_get.return_value = [
        {"id": "1", "text": "Привет", "response": "Здравствуйте!"},
        {"id": "2", "text": "Как дела?", "response": "Хорошо!"}
    ]

    # Мокаем get_current_user
    with patch("api.deps.get_current_user", new_callable=AsyncMock) as mock_user:
        mock_user.return_value.id = 1

        response = await async_client.get("/session/history")
        assert response.status_code == 200
        data = response.json()
        assert "history" in data
        assert len(data["history"]) == 2
        assert data["history"][0]["response"] == "Здравствуйте!"
