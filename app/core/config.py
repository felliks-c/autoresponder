from dotenv import load_dotenv
import os


load_dotenv()

# Пример получения переменной окружения
# MY_VAR = os.getenv("MY_VAR")

SECREYT_KEY = os.getenv("SECRET_KEY")
JWT_ALG = os.getenv("JWT_ALG")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

POSTGRES_DSN = os.getenv("POSTGRES_DSN")
MONGO_DSN = os.getenv("MONGO_DSN")
REDIS_DSN = os.getenv("REDIS_DSN")

SPACY_MODEL = os.getenv("SPACY_MODEL", "ru_core_news_sm") ### NOT FOR DEPLOYMENT!!!

