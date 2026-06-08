from fastapi import APIRouter, Depends
from api.deps import get_current_user
from crud.motor import get_user_messages

router = APIRouter(prefix="/session", tags=["session"])


@router.get("/history")
async def list_messages(user_id: str = Depends(get_current_user)):
    messages = await get_user_messages(user_id)
    return {"user_id": user_id, "history": messages}
