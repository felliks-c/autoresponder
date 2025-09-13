from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
mongo_db = mongo_client[settings.MONGO_DB]
messages_collection = mongo_db["messages"]
