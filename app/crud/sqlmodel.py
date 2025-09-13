from db.models import User, RefreshToken
from sqlmodel import select
from db.postgres import async_session_maker

async def create_user(email: str, hashed_password: str):
    async with async_session_maker() as session:
        user = User(email=email, hashed_password=hashed_password)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

async def get_user_by_email(email: str):
    async with async_session_maker() as session:
        result = await session.exec(select(User).where(User.email == email))
        return result.first()

async def save_refresh_token(user_id: int, token: str):
    async with async_session_maker() as session:
        refresh = RefreshToken(user_id=user_id, token=token)
        session.add(refresh)
        await session.commit()
        return refresh

async def get_user_id_by_refresh_token(token: str):
    async with async_session_maker() as session:
        result = await session.exec(select(RefreshToken).where(RefreshToken.token == token))
        refresh = result.first()
        return refresh.user_id if refresh else None