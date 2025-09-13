import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_login_new_user(async_client: AsyncClient):
    # Мокаем функции create_user и get_user_by_email
    with patch("crud.sqlmodel.get_user_by_email", new_callable=AsyncMock) as mock_get, \
         patch("crud.sqlmodel.create_user", new_callable=AsyncMock) as mock_create, \
         patch("crud.redis.save_access_token", new_callable=AsyncMock) as mock_save_access, \
         patch("crud.sqlmodel.save_refresh_token", new_callable=AsyncMock) as mock_save_refresh:
        
        mock_get.return_value = None
        mock_create.return_value.id = 1
        
        response = await async_client.post("/auth/login", json={
            "email": "newuser@example.com",
            "password": "testpass"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

@pytest.mark.asyncio
async def test_login_existing_user_wrong_password(async_client: AsyncClient):
    user_mock = type("User", (), {"id": 1, "hashed_password": "hashed"})()
    
    with patch("crud.sqlmodel.get_user_by_email", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = user_mock
        
        response = await async_client.post("/auth/login", json={
            "email": "existing@example.com",
            "password": "wrongpass"
        })
        assert response.status_code == 401
