from fastapi import APIRouter, HTTPException
from core.security import create_access_token, create_refresh_token, get_password_hash, verify_password
from crud.sqlmodel import get_user_by_email, create_user, save_refresh_token
from crud.redis import create_session as save_access_token
from core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(email: str, password: str):
    # ищем пользователя
    user = await get_user_by_email(email)

    if not user:
        # если нет — создаём нового
        hashed_pw = get_password_hash(password)
        user = await create_user(email=email, hashed_password=hashed_pw)

    else:
        # если есть — сверяем пароль
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

    # создаём токены
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # сохраняем
    await save_access_token(
        access_token,
        user.id,
        ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    await save_refresh_token(user.id, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
