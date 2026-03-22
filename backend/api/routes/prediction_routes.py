from fastapi import APIRouter, UploadFile, File, Depends
from pydantic import BaseModel, Field
from datetime import datetime
from backend.services.prediction_service import predict_crop, predict_fertilizer, predict_disease
from backend.core.dependencies import get_current_user
from backend.db.mongo_database import get_db

router = APIRouter(prefix="/predict", tags=["predictions"])


class CropFeatures(BaseModel):
    N: float = Field(..., description="Nitrogen")
    P: float = Field(..., description="Phosphorus")
    K: float = Field(..., description="Potassium")
    temperature: float
    humidity: float
    ph: float
    rainfall: float


class FertFeatures(BaseModel):
    temperature: float
    humidity: float
    moisture: float
    soil_type: str
    crop_type: str
    N: float
    P: float
    K: float


@router.post("/crop")
async def crop_endpoint(body: CropFeatures, user: dict = Depends(get_current_user)):
    try:
        result = predict_crop(body.dict())
        db = get_db()
        await db.crop_predictions.insert_one({
            "user_id": user["sub"],
            "inputs": body.dict(),
            "result": result,
            "timestamp": datetime.utcnow(),
        })
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.post("/fertilizer")
async def fertilizer_endpoint(body: FertFeatures, user: dict = Depends(get_current_user)):
    try:
        result = predict_fertilizer(body.dict())
        db = get_db()
        await db.fertilizer_predictions.insert_one({
            "user_id": user["sub"],
            "inputs": body.dict(),
            "result": result,
            "timestamp": datetime.utcnow(),
        })
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.post("/disease")
async def disease_endpoint(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    try:
        img_bytes = await file.read()
        result = predict_disease(img_bytes)
        db = get_db()
        await db.disease_predictions.insert_one({
            "user_id": user["sub"],
            "filename": file.filename,
            "result": result,
            "timestamp": datetime.utcnow(),
        })
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
