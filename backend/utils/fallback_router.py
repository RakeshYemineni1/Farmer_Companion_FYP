import asyncio
import re

def _strip_markdown(text: str) -> str:
    text = re.sub(r'\*+', '', text)        # bold/italic
    text = re.sub(r'#+\s*', '', text)      # headings
    text = re.sub(r'`+', '', text)         # code
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # links
    text = re.sub(r'^[-*]\s+', '', text, flags=re.MULTILINE)  # bullets
    text = re.sub(r'\n{3,}', '\n\n', text) # excess newlines
    return text.strip()

import logging
from backend.core.config import settings
from backend.models.chat_models.gemini_client import GeminiClient

logger = logging.getLogger(__name__)

AGRICULTURE_SYSTEM_PROMPT = (
    "You are KrishiSaathi, an AI farming assistant for Indian farmers. "
    "Be helpful, natural, and concise - like a knowledgeable friend, not a textbook. "
    "Keep responses short and to the point. "
    "IMPORTANT: Never use markdown, asterisks, bold, bullet points, hashtags, or any special characters. "
    "Write in plain conversational text only, like you are texting a friend. "
    "Topics: crops, soil, fertilizers, pests, irrigation, weather, market prices, government schemes. "
    "For plant/crop images: identify the crop, detect any disease or pest, assess severity, and give clear actionable treatment in plain text. "
    "If no disease found, confirm the plant looks healthy. "
    "If question is unrelated to farming, politely redirect. "
    "If asked who you are, say you are KrishiSaathi AI Assistant. "
    "\n\nAlways respond in {language}."
)


def _get_prompt(language: str) -> str:
    lang_names = {
        "en": "English", "hi": "Hindi", "bn": "Bengali", "te": "Telugu",
        "mr": "Marathi", "ta": "Tamil", "gu": "Gujarati", "kn": "Kannada",
        "ml": "Malayalam", "pa": "Punjabi", "or": "Odia",
        "english": "English", "hindi": "Hindi", "bengali": "Bengali",
        "telugu": "Telugu", "marathi": "Marathi", "tamil": "Tamil",
        "gujarati": "Gujarati", "kannada": "Kannada", "malayalam": "Malayalam",
        "punjabi": "Punjabi",
    }
    lang_name = lang_names.get(language.lower(), "English")
    return AGRICULTURE_SYSTEM_PROMPT.format(language=lang_name)


def _build_providers():
    keys = [
        settings.GEMINI_API_KEY,
        settings.GROK_API_KEY,
        settings.OPENROUTER_API_KEY,
    ]
    models = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-2.5-flash-lite"]
    providers = []
    for i, (key, model) in enumerate(zip(keys, models)):
        if key:
            providers.append((f"gemini-{i+1}({model})", GeminiClient(key, model)))
    return providers


class ChatFallbackRouter:
    def __init__(self):
        self.providers = _build_providers()

    async def get_response(self, message: str, image_bytes: bytes = None, language: str = "en") -> dict:
        prompt = _get_prompt(language)
        for name, client in self.providers:
            try:
                response = await asyncio.wait_for(
                    client.chat(message, prompt, image_bytes),
                    timeout=30.0,
                )
                if response:
                    response = _strip_markdown(response)
                    logger.info(f"Chat response served by: {name}")
                    return {"response": response, "provider": name}
            except asyncio.TimeoutError:
                logger.warning(f"{name} timed out, trying next provider")
            except Exception as e:
                logger.warning(f"{name} failed ({e}), trying next provider")

        return {
            "response": "I'm having trouble connecting right now. Please try again in a moment.",
            "provider": "fallback",
        }
