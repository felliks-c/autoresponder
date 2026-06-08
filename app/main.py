from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import session_router, message_router, auth_router
from db.postgres import init_db
from db.mongo import mongo_client
from db.redis import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await mongo_client.admin.command("ping")
    await redis_client.ping()
    yield
    mongo_client.close()
    await redis_client.aclose()


app = FastAPI(title="AsyncApp", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(message_router)
app.include_router(session_router)
