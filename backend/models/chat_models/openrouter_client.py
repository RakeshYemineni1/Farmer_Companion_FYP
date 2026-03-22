import httpx
import base64
from backend.core.config import settings


class OpenRouterClient:
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    async def chat(self, message: str, system_prompt: str, image_bytes: bytes = None) -> str:
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("OpenRouter API key not configured")

        # Use a vision-capable free model
        if image_bytes:
            user_content = [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
                    },
                },
                {"type": "text", "text": message},
            ]
            model = "meta-llama/llama-3.2-11b-vision-instruct:free"
        else:
            user_content = message
            model = "meta-llama/llama-3.3-70b-instruct:free"

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                self.BASE_URL,
                json=payload,
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "HTTP-Referer": "https://krishisaathiii.netlify.app",
                    "X-Title": "KrishiSaathi",
                },
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
