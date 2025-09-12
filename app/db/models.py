from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel
from typing import Optional




class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    hashed_password: str
    is_active: bool = Field(default=True)





class CacheItem(BaseModel):
    key: str
    value: str
    ttl: int = 3600  # Время жизни в секундах (по умолчанию 1 час)





class UserDocument(BaseModel):
    id: Optional[str] = None  # MongoDB использует _id
    name: str
    email: str
    age: int = 0