import os
import io
import numpy as np
import pandas as pd
from joblib import load
from PIL import Image
import tensorflow as tf
from backend.core.config import settings

MODELS_DIR = settings.MODELS_DIR

_crop_model = None
_fert_model = None
_fert_columns = None
_dis_model = None
_dis_labels = ["Healthy", "Powdery Mildew", "Rust Disease"]


def _lazy_crop():
    global _crop_model
    if _crop_model is None:
        _crop_model = load(os.path.join(MODELS_DIR, "crop_model.joblib"))
    return _crop_model


def _lazy_fert():
    global _fert_model, _fert_columns
    if _fert_model is None:
        _fert_model = load(os.path.join(MODELS_DIR, "fertilizer_model.joblib"))
        _fert_columns = load(os.path.join(MODELS_DIR, "fertilizer_model_columns.joblib"))
    return _fert_model, _fert_columns


def _lazy_disease():
    global _dis_model
    if _dis_model is None:
        _dis_model = tf.keras.models.load_model(os.path.join(MODELS_DIR, "disease_model.h5"))
    return _dis_model


def predict_crop(features: dict) -> dict:
    model = _lazy_crop()
    df = pd.DataFrame([features])
    pred = model.predict(df)[0]
    conf = None
    try:
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(df)[0]
            idx = list(model.classes_).index(pred)
            conf = float(proba[idx])
    except Exception:
        pass
    return {"crop": str(pred), "confidence": conf}


def predict_fertilizer(features: dict) -> dict:
    model, columns = _lazy_fert()
    mapped = {
        "Temparature": features["temperature"],
        "Humidity ": features["humidity"],
        "Moisture": features["moisture"],
        "Nitrogen": features["N"],
        "Potassium": features["K"],
        "Phosphorous": features["P"],
    }
    for soil in ["Black", "Clayey", "Loamy", "Red", "Sandy"]:
        mapped[f"Soil Type_{soil}"] = 1 if features["soil_type"] == soil else 0
    for crop in ["Cotton", "Ground Nuts", "Maize", "Millets", "Oil seeds",
                 "Paddy", "Pulses", "Sugarcane", "Tobacco", "Wheat"]:
        mapped[f"Crop Type_{crop}"] = 1 if features["crop_type"] == crop else 0
    df = pd.DataFrame([mapped]).reindex(columns=columns, fill_value=0)
    pred = model.predict(df)[0]
    return {"fertilizer": str(pred)}


def predict_disease(image_bytes: bytes) -> dict:
    model = _lazy_disease()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((224, 224))
    arr = np.array(img) / 255.0
    arr = arr[None, ...]
    probs = model.predict(arr, verbose=0)[0]
    idx = int(np.argmax(probs))
    confidence = float(probs[idx])
    disease = _dis_labels[idx]

    if disease == "Healthy":
        final_class = "Healthy"
        severity = "None"
    elif confidence >= 0.85:
        final_class = f"{disease} - Early"
        severity = "Early"
    elif confidence >= 0.65:
        final_class = f"{disease} - Moderate"
        severity = "Moderate"
    else:
        final_class = f"{disease} - Severe"
        severity = "Severe"

    return {
        "disease": final_class,
        "base_disease": disease,
        "confidence": confidence,
        "severity": severity,
    }
