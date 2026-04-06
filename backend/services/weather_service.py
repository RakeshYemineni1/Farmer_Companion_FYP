import httpx
from datetime import datetime
from backend.core.config import settings
from backend.models.chat_models.gemini_client import GeminiClient


async def _get_gemini_advisory(weather_summary: str, location: str) -> str:
    keys = [settings.GEMINI_API_KEY, settings.GROK_API_KEY, settings.OPENROUTER_API_KEY]
    models = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-2.5-flash-lite"]

    prompt = (
        "You are KrishiSaathi, an AI farming assistant for Indian farmers. "
        "Based on the weather forecast below, give 3-5 short, practical farming advisories in plain text. "
        "No markdown, no bullet symbols, no asterisks. Each advice on a new line. Be concise and actionable."
    )
    message = f"Location: {location}\nWeather forecast:\n{weather_summary}"

    for key, model in zip(keys, models):
        if not key:
            continue
        try:
            client = GeminiClient(key, model)
            return await client.chat(message, prompt)
        except Exception:
            continue

    return "Check local conditions before farming activities."


async def get_weather_and_advisory(lat: float, lon: float, user_id: str, db) -> dict:
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Open-Meteo: free, no API key required
        geo_r = await client.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "json"},
            headers={"User-Agent": "KrishiSaathi/2.0"},
        )
        location = "Your Location"
        if geo_r.status_code == 200:
            geo = geo_r.json()
            location = geo.get("address", {}).get("city") or geo.get("address", {}).get("town") or geo.get("address", {}).get("village") or geo.get("display_name", "Your Location").split(",")[0]

        weather_r = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,relative_humidity_2m_max",
                "timezone": "Asia/Kolkata",
                "forecast_days": 7,
            },
        )
        weather_r.raise_for_status()
        data = weather_r.json()

    daily = data["daily"]
    forecast = []
    summary_lines = []

    for i in range(len(daily["time"])):
        temp_max = daily["temperature_2m_max"][i]
        temp_min = daily["temperature_2m_min"][i]
        rain = daily["precipitation_sum"][i] or 0
        wind = daily["windspeed_10m_max"][i] or 0
        humidity = daily["relative_humidity_2m_max"][i] or 0
        date = daily["time"][i]

        day = {
            "date": date,
            "temp_max": temp_max,
            "temp_min": temp_min,
            "humidity": humidity,
            "rain_mm": rain,
            "wind_kmh": wind,
        }
        forecast.append(day)
        summary_lines.append(
            f"{date}: max {temp_max}°C, min {temp_min}°C, rain {rain}mm, wind {wind}km/h, humidity {humidity}%"
        )

    advisory = await _get_gemini_advisory("\n".join(summary_lines), location)

    result = {
        "location": location,
        "forecast": forecast,
        "gemini_advisory": advisory,
    }

    await db.weather_history.insert_one({
        "user_id": user_id,
        "lat": lat,
        "lon": lon,
        "location": location,
        "forecast": forecast,
        "gemini_advisory": advisory,
        "timestamp": datetime.utcnow(),
    })

    return result
