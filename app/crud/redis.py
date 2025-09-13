from typing import Optional
from db.redis import redis_client


SESSION_EXPIRE_SECONDS = 60 * 60  # 60 минут


# Создать сессию (сохранить токен → user_id)
async def create_session(token: str, user_id: str) -> bool:
    """
    Создает запись в Redis вида: token -> user_id
    Живет 60 минут.
    """
    result = await redis_client.set(
        token,
        user_id,
        ex=SESSION_EXPIRE_SECONDS
    )
    return result is True  # вернет True если ок


# Получить user_id по токену
async def get_user_by_token(token: str) -> Optional[str]:
    """
    Возвращает user_id по токену, если сессия существует.
    """
    return await redis_client.get(token)


# Удалить сессию по токену (логаут)
async def delete_session(token: str) -> bool:
    """
    Удаляет запись token -> user_id.
    """
    result = await redis_client.delete(token)
    return result == 1  # 1 если удалилось, 0 если не было


# Обновить TTL у сессии (продлить жизнь токена)
async def refresh_session(token: str) -> bool:
    """
    Обновляет TTL на 60 минут.
    """
    result = await redis_client.expire(token, SESSION_EXPIRE_SECONDS)
    return result is True
