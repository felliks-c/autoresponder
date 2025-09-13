from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional

from crud.motor import create_message
from crud.redis import get_user_by_token
from crud.sqlmodel import get_user_id_by_refresh_token
from nlp.pipeline import nlp_pipeline

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/send")
async def add_message(
    text: str,
    authorization: Optional[str] = Header(None)  # токен будем брать из заголовка Authorization
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token required")

    # Обычно токен приходит в формате "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    token = parts[1]

    # 1. Пробуем найти user_id по access token в Redis
    user_id = await get_user_by_token(token)

    # 2. Если не нашли — пробуем refresh token в Postgres
    if not user_id:
        user_id = await get_user_id_by_refresh_token(token)

    # 3. Если всё ещё нет — отказ
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Access denied. Please re-login or use a refresh token."
        )

    # 4. Пропускаем через NLP пайплайн
    response, typ = await nlp_pipeline(text)

    # 5. Логируем сообщение в MongoDB
    await create_message(
        user_id=str(user_id),
        text=text,
        typ=typ,
        response=response,
        status="saved"
    )

    # 6. Возвращаем ответ пользователю
    return {"response": response}



