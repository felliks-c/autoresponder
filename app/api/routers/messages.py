# app/api/routers/messages.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
from app.api.deps import get_nlp, get_mongo
from app.core.security import get_current_user
from app.db.postgres import get_session
from app.db.models import MessageHistory

router = APIRouter()

class MessageIn(BaseModel):
    text: str

@router.post("/send")
async def send_message(body: MessageIn, user=Depends(get_current_user), nlp=Depends(get_nlp), mongo=Depends(get_mongo)):
    user_id, _ = user
    # лог сырого в Mongo
    await mongo.raw_messages.insert_one({"user_id": user_id, "text": body.text, "created_at": datetime.utcnow()})

    intent, conf = nlp.classify(body.text)
    resp = nlp.respond(intent)

    # сохранить историю в Postgres
    async with get_session() as s:
        s.add(MessageHistory(user_id=user_id, text=body.text, intent=intent, response=resp))
        await s.commit()

    # если unknown — лог в Mongo
    if intent == "unknown":
        await mongo.unknown_logs.insert_one({"user_id": user_id, "text": body.text, "reason": "no_match", "created_at": datetime.utcnow()})
    else:
        await mongo.classified_intents.insert_one({"user_id": user_id, "text": body.text, "intent": intent, "confidence": conf, "created_at": datetime.utcnow()})

    return {"intent": intent, "response": resp}
