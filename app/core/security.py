# app/core/security.py
import time, uuid, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.db.redis import get_redis

bearer = HTTPBearer(auto_error=True)

def create_access_token(user_id: int) -> dict:
    jti = str(uuid.uuid4())
    now = int(time.time())
    exp = now + settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    payload = {"sub": str(user_id), "jti": jti, "exp": exp, "iat": now}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALG)
    return {"access_token": token, "jti": jti, "exp": exp}

async def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        payload = jwt.decode(creds.credentials, settings.SECRET_KEY, algorithms=[settings.JWT_ALG])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    jti = payload.get("jti")
    if not jti:
        raise HTTPException(status_code=401, detail="Invalid token")
    r = await get_redis()
    if not await r.exists(f"session:{jti}"):
        raise HTTPException(status_code=401, detail="Session expired")
    return int(payload["sub"]), jti
