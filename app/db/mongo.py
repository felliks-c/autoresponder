from motor.motor_asyncio import AsyncIOMotorClient

# Шаблонный URL подключения (замените user, password, host)
MONGO_URL = "mongodb://user:password@host:27017/db_name?authSource=admin"

# Создание клиента
client = AsyncIOMotorClient(MONGO_URL)
db = client["db_name"]  # Имя вашей БД

# Функция для получения БД (для Dependency Injection)
async def get_mongo_db():
    try:
        yield db
    finally:
        pass  # Motor не требует явного закрытия