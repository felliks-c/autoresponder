from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    age: int = Field(default=0)






from pydantic import BaseModel

class CacheItem(BaseModel):
    key: str
    value: str
    ttl: int = 3600  # Время жизни в секундах (по умолчанию 1 час)











from pydantic import BaseModel
from typing import Optional

class UserDocument(BaseModel):
    id: Optional[str] = None  # MongoDB использует _id
    name: str
    email: str
    age: int = 0