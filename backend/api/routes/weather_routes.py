from fastapi import APIRouter, Depends
from backend.services.weather_service import get_weather_and_advisory
from backend.core.dependencies import get_current_user
from backend.db.mongo_database import get_db

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/forecast")
async def weather_forecast(
    lat: float,
    lon: float,
    user: dict = Depends(get_current_user)
):
    db = get_db()
    result = await get_weather_and_advisory(lat, lon, user["sub"], db)
    return result
