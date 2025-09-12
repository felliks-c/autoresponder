from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import async_session_maker # Импортируем нашу фабрику
from jose import JWTError, jwt
from datetime import datetime, timedelta
from core.config import SECRET_KEY, JWT_ALG as ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Эта функция-зависимость создает асинхронную сессию для работы с БД.
    Она будет использоваться в эндпоинтах FastAPI.
    """
    async with async_session_maker() as session:
        yield session



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)