from typing import Optional
from db.redis import redis_client

SESSION_EXPIRE_SECONDS = 60 * 60  # fallback: 60 minutes


async def create_session(token: str, user_id: str, ttl: int = SESSION_EXPIRE_SECONDS) -> bool:
    result = await redis_client.set(token, user_id, ex=ttl)
    return result is True


async def get_user_by_token(token: str) -> Optional[str]:
    return await redis_client.get(token)


async def delete_session(token: str) -> bool:
    result = await redis_client.delete(token)
    return result == 1


async def refresh_session(token: str, ttl: int = SESSION_EXPIRE_SECONDS) -> bool:
    result = await redis_client.expire(token, ttl)
    return result is True
