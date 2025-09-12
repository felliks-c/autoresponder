import json

# CRUD для простых ключей (строки/JSON)
async def create_key(redis: aioredis.Redis, key: str, value: str, ttl: int = None):
    await redis.set(key, value)
    if ttl:
        await redis.expire(key, ttl)
    return True

async def read_key(redis: aioredis.Redis, key: str):
    return await redis.get(key)

async def update_key(redis: aioredis.Redis, key: str, value: str, ttl: int = None):
    return await create_key(redis, key, value, ttl)  # Update = перезапись

async def delete_key(redis: aioredis.Redis, key: str):
    return await redis.delete(key) > 0

# CRUD для хэшей (аналог объекта с полями)
async def create_hash(redis: aioredis.Redis, hash_key: str, field: str, value: str):
    await redis.hset(hash_key, field, value)
    return True

async def read_hash(redis: aioredis.Redis, hash_key: str, field: str = None):
    if field:
        return await redis.hget(hash_key, field)
    return await redis.hgetall(hash_key)

async def update_hash(redis: aioredis.Redis, hash_key: str, field: str, value: str):
    return await create_hash(redis, hash_key, field, value)

async def delete_hash_field(redis: aioredis.Redis, hash_key: str, field: str):
    return await redis.hdel(hash_key, field) > 0

# Пример с JSON (используя Pydantic для валидации)
async def create_json(redis: aioredis.Redis, key: str, data: dict):
    validated = CacheItem(**data)  # Валидация
    await redis.set(key, json.dumps(validated.dict()))
    return True

# Пример в FastAPI
from fastapi import FastAPI, Depends

app = FastAPI()

@app.post("/cache/{key}")
async def add_cache(key: str, value: str, redis: aioredis.Redis = Depends(get_redis)):
    await create_key(redis, key, value)
    return {"status": "ok"}