from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings


load_dotenv()


SECREYT_KEY = os.getenv("SECRET_KEY")
JWT_ALG = os.getenv("JWT_ALG")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

POSTGRES_DSN = os.getenv("POSTGRES_DSN")
MONGO_DSN = os.getenv("MONGO_DSN")
REDIS_DSN = os.getenv("REDIS_DSN")
MONGO_DB = os.getenv("MONGO_DB")

SPACY_MODEL = os.getenv("SPACY_MODEL", "ru_core_news_sm") ### NOT FOR DEPLOYMENT!!!





class Settings(BaseSettings):
    APP_NAME: str = "AsyncApp"
    DATABASE_URL: str = POSTGRES_DSN
    MONGO_URL: str = MONGO_DSN
    MONGO_DB: str = MONGO_DB
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    SECRET_KEY: str = "supersecret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"

settings = Settings()
