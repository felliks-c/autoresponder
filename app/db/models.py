from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str
    created_at: datetime = Field(default_factory=_utcnow)


class RefreshToken(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token: str
    created_at: datetime = Field(default_factory=_utcnow)
