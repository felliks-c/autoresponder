from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

from crud.motor import create_message
from crud.redis import get_user_by_token
from crud.sqlmodel import get_user_id_by_refresh_token
from core.security import decode_token
from nlp.pipeline import nlp_pipeline

router = APIRouter(prefix="/messages", tags=["messages"])


class MessageRequest(BaseModel):
    text: str


@router.post("/send")
async def add_message(
    body: MessageRequest,
    authorization: Optional[str] = Header(None),
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token required")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    token = parts[1]

    # Try access token in Redis first
    user_id = await get_user_by_token(token)

    # Fall back to refresh token in Postgres (only if token is actually a refresh type)
    if not user_id:
        payload = decode_token(token)
        if payload and payload.get("type") == "refresh":
            db_user_id = await get_user_id_by_refresh_token(token)
            if db_user_id:
                user_id = str(db_user_id)

    if not user_id:
        raise HTTPException(status_code=401, detail="Access denied. Please re-login.")

    response, typ = await nlp_pipeline(body.text)

    await create_message(
        user_id=str(user_id),
        text=body.text,
        typ=typ,
        response=response,
        status="saved",
    )

    return {"response": response}
