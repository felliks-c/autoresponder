import redis.asyncio as aioredis

# Шаблонный URL подключения (замените host, port, password)
REDIS_URL = "redis://:password@host:6379/0"

# Создание пула соединений (для переиспользования)
async def get_redis():
    redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    try:
        yield redis
    finally:
        await redis.close()