from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.security import create_access_token, create_refresh_token, get_password_hash, verify_password
from crud.sqlmodel import get_user_by_email, create_user, save_refresh_token
from crud.redis import create_session
from core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(body: LoginRequest):
    user = await get_user_by_email(body.email)

    if not user:
        hashed_pw = get_password_hash(body.password)
        user = await create_user(email=body.email, hashed_password=hashed_pw)
        if not user:
            raise HTTPException(status_code=500, detail="Failed to create user")
    else:
        if not verify_password(body.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    await create_session(access_token, str(user.id), ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    await save_refresh_token(user.id, refresh_token)

    return {"access_token": access_token, "refresh_token": refresh_token}
