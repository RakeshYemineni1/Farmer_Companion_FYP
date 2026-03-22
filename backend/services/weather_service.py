import httpx
from datetime import datetime
from backend.core.config import settings

FARMING_ADVISORIES = [
    {
        "condition": lambda d: d["humidity"] > 80,
        "advice": "High humidity detected — risk of fungal diseases. Consider fungicide application.",
    },
    {
        "condition": lambda d: d["rain_mm"] > 20,
        "advice": "Heavy rain expected — delay fertilizer application to avoid nutrient runoff.",
    },
    {
        "condition": lambda d: d["rain_mm"] == 0 and d["temp"] > 32,
        "advice": "Hot and dry conditions — irrigation recommended today.",
    },
    {
        "condition": lambda d: d["wind_kmh"] > 40,
        "advice": "Strong winds forecast — avoid pesticide spraying today.",
    },
    {
        "condition": lambda d: d["temp"] < 10,
        "advice": "Cold temperatures — protect sensitive crops from frost damage.",
    },
    {
        "condition": lambda d: 20 <= d["rain_mm"] <= 40,
        "advice": "Moderate rainfall expected — good conditions for sowing.",
    },
]


async def get_weather_and_advisory(lat: float, lon: float, user_id: str, db) -> dict:
    if not settings.OPENWEATHER_API_KEY:
        return {"error": "Weather API key not configured"}

    async with httpx.AsyncClient(timeout=8.0) as client:
        r = await client.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={
                "lat": lat,
                "lon": lon,
                "appid": settings.OPENWEATHER_API_KEY,
                "units": "metric",
                "cnt": 7,
            },
        )
        r.raise_for_status()
        data = r.json()

    forecast = []
    for item in data["list"]:
        day = {
            "date": item["dt_txt"],
            "temp": item["main"]["temp"],
            "humidity": item["main"]["humidity"],
            "rain_mm": item.get("rain", {}).get("3h", 0),
            "wind_kmh": round(item["wind"]["speed"] * 3.6, 1),
            "description": item["weather"][0]["description"],
            "icon": item["weather"][0]["icon"],
        }
        day["advisories"] = [
            a["advice"] for a in FARMING_ADVISORIES if a["condition"](day)
        ]
        forecast.append(day)

    result = {"location": data["city"]["name"], "forecast": forecast}

    # Persist to MongoDB
    await db.weather_history.insert_one({
        "user_id": user_id,
        "lat": lat,
        "lon": lon,
        "location": result["location"],
        "forecast": forecast,
        "timestamp": datetime.utcnow(),
    })

    return result
