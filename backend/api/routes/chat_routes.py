from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import Optional
from backend.services.chat_service import handle_chat
from backend.core.dependencies import get_current_user
from backend.db.mongo_database import get_db

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
async def chat(
    message: str = Form(...),
    language: str = Form(default="en"),
    image: Optional[UploadFile] = File(default=None),
    user: dict = Depends(get_current_user),
):
    db = get_db()
    image_bytes = await image.read() if image else None
    result = await handle_chat(
        message=message,
        language=language,
        user_id=user["sub"],
        db=db,
        image_bytes=image_bytes,
    )
    return {"success": True, **result}


@router.post("/speech")
async def speech_chat(
    text: str = Form(...),
    language: str = Form(default="english"),
    user: dict = Depends(get_current_user),
):
    """Accepts transcribed speech text, returns response in same language."""
    db = get_db()
    result = await handle_chat(
        message=text,
        language=language,
        user_id=user["sub"],
        db=db,
    )
    return {"success": True, **result}


@router.get("/history")
async def chat_history(user: dict = Depends(get_current_user), limit: int = 20):
    db = get_db()
    cursor = db.chat_history.find(
        {"user_id": user["sub"]},
        {"_id": 0, "user_message": 1, "bot_response": 1, "language": 1,
         "provider_used": 1, "has_image": 1, "timestamp": 1}
    ).sort("timestamp", -1).limit(limit)
    history = await cursor.to_list(length=limit)
    return {"history": history}
