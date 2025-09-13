from fastapi import FastAPI
from api.routers import session_router, message_router, auth_router
from db.postgres import init_db
from db.mongo import mongo_client
from db.redis import redis_client

app = FastAPI(title="AsyncApp", version="1.0")




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await mongo_client.admin.command("ping")
    await redis_client.ping()

    yield
    # Shutdown
    mongo_client.close()
    await redis_client.close()



app.include_router(auth_router)
app.include_router(message_router)
app.include_router(session_router)