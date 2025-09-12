from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from sqlmodel import select
from core.config import POSTGRES_DSN as DATABASE_URL


# Создание асинхронного engine
engine = create_engine(DATABASE_URL, echo=True, future=True)  # echo=True для логирования запросов


# Создать базу (один раз, при инициализации)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


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