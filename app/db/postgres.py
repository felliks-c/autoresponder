# app/db/models.py
# from sqlmodel import SQLModel, Field, Relationship
# from typing import Optional
# from datetime import datetime
# import uuid

# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     email: str = Field(index=True, unique=True)
#     password_hash: str
#     is_active: bool = True
#     created_at: datetime = Field(default_factory=datetime.utcnow)

# class MessageHistory(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: int = Field(foreign_key="user.id", index=True)
#     text: str
#     intent: str
#     response: str
#     created_at: datetime = Field(default_factory=datetime.utcnow)

# class SessionHistory(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: int = Field(foreign_key="user.id", index=True)
#     jti: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True)
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     revoked: bool = False


from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

# Шаблонный URL подключения (замените user, password, host, db_name)
DATABASE_URL = "postgresql+asyncpg://user:password@host:5432/db_name"

# Создание асинхронного engine
engine = create_engine(DATABASE_URL, echo=True, future=True)  # echo=True для логирования запросов

# Функция для получения сессии (для Dependency Injection в FastAPI)
async def get_session():
    async_session = AsyncSession(engine)
    try:
        yield async_session
        await async_session.commit()
    except Exception:
        await async_session.rollback()
        raise
    finally:
        await async_session.close()