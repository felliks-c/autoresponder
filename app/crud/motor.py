from typing import Optional, List
from bson import ObjectId
from db.mongo import messages_collection


# вставка сообщения
async def create_message(user_id: str, text: str, typ: str, response: str, status: str) -> str:
    doc = {
        "user_id": user_id,
        "text": text,
        "intent": {
            "type": typ,
            "response": response
        },
        "status": status
    }
    result = await messages_collection.insert_one(doc)
    return str(result.inserted_id)  # возвращаем строковый _id


# получение одного сообщения по _id
async def get_message(message_id: str) -> Optional[dict]:
    try:
        oid = ObjectId(message_id)
    except Exception:
        return None  # некорректный id

    doc = await messages_collection.find_one({"_id": oid})
    if doc:
        return {
            "id": str(doc["_id"]),
            "user_id": doc["user_id"],
            "text": doc["text"],
            "intent": doc["intent"],
            "status": doc["status"],
        }
    return None


# получение всех сообщений пользователя
async def get_user_messages(user_id: str) -> List[dict]:
    cursor = messages_collection.find({"user_id": user_id})
    docs = await cursor.to_list(length=100)  # ограничение на количество
    return [
        {
            "id": str(d["_id"]),
            "text": d["text"],
            "response": d["intent"]["response"]
        }
        for d in docs
    ]
