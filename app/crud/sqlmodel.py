from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from db.postgres import engine
from db.models import User


# Добавление
async def create_user(session: AsyncSession, email: str, password: str):
    user = User(email=email, hashed_password=password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

# Получение
async def get_user_by_email(session: AsyncSession, email: str):
    result = await session.exec(select(User).where(User.email == email))
    return result.first()
















# CRUD-функции (используйте в async-контексте, например, в FastAPI с depends(get_session))
async def create_user(session: AsyncSession, user: User):
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def read_user(session: AsyncSession, user_id: int):
    query = select(User).where(User.id == user_id)
    result = await session.exec(query)
    return result.first()

async def update_user(session: AsyncSession, user_id: int, name: str, age: int):
    user = await read_user(session, user_id)
    if user:
        user.name = name
        user.age = age
        await session.commit()
        await session.refresh(user)
        return user
    return None

async def delete_user(session: AsyncSession, user_id: int):
    user = await read_user(session, user_id)
    if user:
        await session.delete(user)
        await session.commit()
        return True
    return False

# Пример использования в FastAPI
from fastapi import FastAPI, Depends

app = FastAPI()

@app.post("/users/")
async def add_user(user: User, session: AsyncSession = Depends(get_session)):
    return await create_user(session, user)