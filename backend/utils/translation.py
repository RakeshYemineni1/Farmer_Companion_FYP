import httpx
import urllib.parse
import logging

logger = logging.getLogger(__name__)

# In-memory cache: (text, target_lang) -> translated_text
_cache: dict = {}


async def _google_translate(text: str, source: str, target: str) -> str:
    """Calls the free Google Translate endpoint."""
    cache_key = (text[:200], source, target)
    if cache_key in _cache:
        return _cache[cache_key]

    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": source,
        "tl": target,
        "dt": "t",
        "q": text,
    }
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            result = r.json()
            translated = "".join(part[0] for part in result[0] if part[0])
            _cache[cache_key] = translated
            return translated
    except Exception as e:
        logger.warning(f"Translation failed ({source}->{target}): {e}")
        return text  # fallback: return original


# Language code map: chatbot language name -> ISO 639-1
LANG_CODE_MAP = {
    "english": "en",
    "hindi": "hi",
    "bengali": "bn",
    "telugu": "te",
    "marathi": "mr",
    "tamil": "ta",
    "gujarati": "gu",
    "kannada": "kn",
    "malayalam": "ml",
    "punjabi": "pa",
    "odia": "or",
    # also accept ISO codes directly
    "en": "en", "hi": "hi", "bn": "bn", "te": "te",
    "mr": "mr", "ta": "ta", "gu": "gu", "kn": "kn",
    "ml": "ml", "pa": "pa", "or": "or",
}


def _resolve(language: str) -> str:
    return LANG_CODE_MAP.get(language.lower(), "en")


async def translate_to_english(text: str, language: str) -> str:
    lang_code = _resolve(language)
    if lang_code == "en":
        return text
    return await _google_translate(text, lang_code, "en")


async def translate_from_english(text: str, language: str) -> str:
    lang_code = _resolve(language)
    if lang_code == "en":
        return text
    return await _google_translate(text, "en", lang_code)
