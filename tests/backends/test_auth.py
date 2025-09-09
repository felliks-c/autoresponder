# tests/test_auth.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_login_ok():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/auth/login", json={"username":"admin","password":"admin"})
        assert r.status_code == 200
        assert "access_token" in r.json()
