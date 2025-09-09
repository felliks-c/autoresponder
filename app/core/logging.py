# app/api/routers/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.hash import bcrypt
from sqlmodel import select
from app.core.security import create_access_token
from app.db.postgres import get_session
from app.db.redis import get_redis
from app.db.models import User, SessionHistory

router = APIRouter()

class LoginIn(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(body: LoginIn):
    # демо: захардкожено
    if not (body.username == "admin" and body.password == "admin"):
        raise HTTPException(status_code=401, detail="Bad credentials")

    # допустим user_id=1
    user_id = 1
    tok = create_access_token(user_id)
    # session persist
    r = await get_redis()
    ttl = tok["exp"] - int(__import__("time").time())
    await r.setex(f"session:{tok['jti']}", ttl, str(user_id))

    async with get_session() as s:
        s.add(SessionHistory(user_id=user_id, jti=tok["jti"]))
        await s.commit()

    return {"access_token": tok["access_token"], "token_type": "bearer"}
