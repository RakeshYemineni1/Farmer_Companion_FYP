from datetime import datetime
from backend.utils.fallback_router import ChatFallbackRouter

_router = ChatFallbackRouter()


async def handle_chat(message: str, language: str, user_id: str, db, image_bytes: bytes = None) -> dict:
    # Gemini responds directly in the target language — no translation needed
    result = await _router.get_response(message, image_bytes, language)

    await db.chat_history.insert_one({
        "user_id": user_id,
        "user_message": message,
        "bot_response": result["response"],
        "language": language,
        "provider_used": result["provider"],
        "has_image": image_bytes is not None,
        "timestamp": datetime.utcnow(),
    })

    return {"response": result["response"], "provider": result["provider"]}
