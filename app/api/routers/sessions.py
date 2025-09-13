from fastapi import APIRouter, Depends
from api.deps import get_current_user
from crud.motor import get_user_messages

router = APIRouter(prefix="/session", tags=["session"])


@router.get("/history")
async def list_messages(user=Depends(get_current_user)):
    """
    История сообщений текущего пользователя
    """
    user_id = str(user.id)  # приводим к str, чтобы совпадало с Mongo user_id
    messages = await get_user_messages(user_id)

    return {
        "user_id": user_id,
        "history": messages
    }
