from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AsyncApp"

    DATABASE_URL: str = Field(validation_alias="POSTGRES_DSN")
    MONGO_URL: str = Field(validation_alias="MONGO_DSN")
    MONGO_DB: str = "appdb"

    REDIS_URL: str = Field(default="redis://localhost:6379/0", validation_alias="REDIS_DSN")

    SECRET_KEY: str
    ALGORITHM: str = Field(default="HS256", validation_alias="JWT_ALG")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        populate_by_name=True,
        extra="ignore",
    )


settings = Settings()
