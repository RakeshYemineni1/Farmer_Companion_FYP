import httpx
import base64
from backend.core.config import settings

GEMINI_MODELS = [
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-1.0-pro",
]


class GeminiClient:
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    async def chat(self, message: str, system_prompt: str, image_bytes: bytes = None) -> str:
        if not self.api_key:
            raise ValueError("Gemini API key not configured")

        if image_bytes:
            parts = [
                {"text": system_prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(image_bytes).decode("utf-8")}},
                {"text": f"Analyze this plant/crop image. Identify: 1) crop type, 2) any disease or pest (name it), 3) severity, 4) treatment steps. User also says: {message}"},
            ]
        else:
            parts = [{"text": f"{system_prompt}\n\nUser: {message}"}]

        payload = {"contents": [{"parts": parts}]}

        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                self.BASE_URL.format(model=self.model) + f"?key={self.api_key}",
                json=payload
            )
            r.raise_for_status()
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
