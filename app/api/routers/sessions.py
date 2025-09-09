# app/api/routers/sessions.py
from fastapi import APIRouter, Depends
from sqlmodel import select
from app.core.security import get_current_user
from app.db.postgres import get_session
from app.db.models import MessageHistory

router = APIRouter()

@router.get("/history")
async def history(user=Depends(get_current_user)):
    user_id, _ = user
    async with get_session() as s:
        res = await s.exec(select(MessageHistory).where(MessageHistory.user_id == user_id).order_by(MessageHistory.created_at.desc()))
        rows = res.all()
    return [{"text": r.text, "intent": r.intent, "response": r.response, "created_at": r.created_at.isoformat()} for r in rows]
