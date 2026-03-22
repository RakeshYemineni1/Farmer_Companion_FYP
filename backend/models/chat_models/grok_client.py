import httpx
import base64
from backend.core.config import settings


class GrokClient:
    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

    async def chat(self, message: str, system_prompt: str, image_bytes: bytes = None) -> str:
        if not settings.GROK_API_KEY:
            raise ValueError("Groq API key not configured")

        # Groq doesn't support vision, fall back to text only
        user_content = message

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                self.BASE_URL,
                json=payload,
                headers={"Authorization": f"Bearer {settings.GROK_API_KEY}"},
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
