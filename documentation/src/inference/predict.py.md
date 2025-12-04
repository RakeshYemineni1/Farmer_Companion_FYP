# src/inference/predict.py

## 📋 Overview
Machine learning inference module that provides prediction functions for crop recommendation, fertilizer suggestion, and plant disease detection using pre-trained models.

## 🎯 Purpose
- Load and manage trained ML models
- Provide prediction interfaces for API endpoints
- Handle model-specific data preprocessing
- Return structured prediction results with confidence scores

## 🏗️ Model Management

### Lazy Loading Pattern
```python
# Global model variables
_crop_model = None
_fert_model = None
_fert_columns = None
_dis_model = None
_dis_labels = None

def _lazy_crop():
    global _crop_model
    if _crop_model is None:
        _crop_model = load(os.path.join(MODELS_DIR, "crop_model.joblib"))
    return _crop_model
```

### Model Directory Configuration
```python
MODELS_DIR = os.getenv("MODELS_DIR", "new model")
```

## 🌾 Crop Recommendation

### Function: predict_crop()
```python
def predict_crop(features: dict) -> dict:
    model = _lazy_crop()
    import pandas as pd
    df = pd.DataFrame([features])
    pred = model.predict(df)[0]
    
    # Get confidence if available
    conf = None
    try:
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(df)[0]
            idx = list(model.classes_).index(pred)
            conf = float(proba[idx])
    except:
        pass
    
    return {"crop": str(pred), "confidence": conf}
```

### Input Features
```python
{
    "N": 90,           # Nitrogen content
    "P": 42,           # Phosphorus content  
    "K": 43,           # Potassium content
    "temperature": 20.87,  # Temperature in Celsius
    "humidity": 82.00,     # Humidity percentage
    "ph": 6.50,           # Soil pH level
    "rainfall": 202.93    # Rainfall in mm
}
```

### Output Format
```python
{
    "crop": "rice",        # Recommended crop name
    "confidence": 0.99     # Prediction confidence (0-1)
}
```

## 💧 Fertilizer Recommendation

### Function: predict_fertilizer()
```python
def predict_fertilizer(features: dict) -> dict:
    model, columns = _lazy_fert()
    
    # Map input features to model's expected format
    mapped_data = {
        'Temparature': features['temperature'],
        'Humidity ': features['humidity'], 
        'Moisture': features['moisture'],
        'Nitrogen': features['N'],
        'Potassium': features['K'],
        'Phosphorous': features['P']
    }
    
    # One-hot encode categorical features
    # ... encoding logic ...
    
    pred = model.predict(df)[0]
    return {"fertilizer": str(pred)}
```

### Feature Mapping
```python
# Input to model mapping
mapped_data = {
    'Temparature': features['temperature'],      # Note: typo in original dataset
    'Humidity ': features['humidity'],           # Note: space in original dataset
    'Moisture': features['moisture'],
    'Nitrogen': features['N'],
    'Potassium': features['K'],
    'Phosphorous': features['P']
}
```

### Categorical Encoding
```python
# Soil type one-hot encoding
soil_types = ['Clayey', 'Loamy', 'Red', 'Sandy']
for soil in soil_types:
    mapped_data[f'Soil Type_{soil}'] = 1 if features['soil_type'] == soil else 0

# Crop type one-hot encoding
crop_types = ['Cotton', 'Ground Nuts', 'Maize', 'Millets', 'Oil seeds', 
              'Paddy', 'Pulses', 'Sugarcane', 'Tobacco', 'Wheat']
for crop in crop_types:
    mapped_data[f'Crop Type_{crop}'] = 1 if features['crop_type'] == crop else 0
```

### Input Features
```python
{
    "temperature": 26.0,
    "humidity": 52.0,
    "moisture": 38.0,
    "soil_type": "Loamy",      # One of: Clayey, Loamy, Red, Sandy
    "crop_type": "Maize",      # One of supported crop types
    "N": 37,                   # Current nitrogen level
    "P": 0,                    # Current phosphorus level
    "K": 0                     # Current potassium level
}
```

## 🦠 Disease Detection

### Function: predict_disease()
```python
def predict_disease(image_bytes: bytes) -> dict:
    model, labels = _lazy_disease()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((224,224))
    arr = np.array(img) / 255.0  # Normalize to [0,1]
    arr = arr[None, ...]  # Add batch dimension
    probs = model.predict(arr, verbose=0)[0]
    idx = int(np.argmax(probs))
    confidence = float(probs[idx])
    disease = labels[idx]
    
    # Severity mapping based on confidence
    if disease == 'Healthy':
        final_class = 'Healthy'
    elif confidence >= 0.85:
        final_class = f'{disease} - Early'
    elif confidence >= 0.65:
        final_class = f'{disease} - Moderate'
    else:
        final_class = f'{disease} - Severe'
    
    return {
        "disease": final_class,
        "base_disease": disease,
        "confidence": confidence,
        "severity": "None" if disease == 'Healthy' else final_class.split(' - ')[1]
    }
```

### Image Processing Pipeline
1. **Load Image**: From bytes using PIL
2. **Convert**: To RGB format
3. **Resize**: To 224x224 pixels (MobileNetV2 input size)
4. **Normalize**: Pixel values to [0,1] range
5. **Batch**: Add batch dimension for model input

### Disease Classes
```python
_dis_labels = ['Healthy', 'Powdery Mildew', 'Rust Disease']
```

### Severity Classification
```python
# Confidence-based severity mapping
if confidence >= 0.85:
    severity = "Early"      # High confidence = early detection
elif confidence >= 0.65:
    severity = "Moderate"   # Medium confidence = moderate stage
else:
    severity = "Severe"     # Low confidence = advanced stage
```

### Output Format
```python
{
    "disease": "Powdery Mildew - Early",    # Disease with severity
    "base_disease": "Powdery Mildew",       # Base disease class
    "confidence": 0.87,                     # Model confidence
    "severity": "Early"                     # Severity level
}
```

## 🔧 Model Loading Functions

### Crop Model Loading
```python
def _lazy_crop():
    global _crop_model
    if _crop_model is None:
        _crop_model = load(os.path.join(MODELS_DIR, "crop_model.joblib"))
    return _crop_model
```

### Fertilizer Model Loading
```python
def _lazy_fert():
    global _fert_model, _fert_columns
    if _fert_model is None:
        _fert_model = load(os.path.join(MODELS_DIR, "fertilizer_model.joblib"))
        _fert_columns = load(os.path.join(MODELS_DIR, "fertilizer_model_columns.joblib"))
    return _fert_model, _fert_columns
```

### Disease Model Loading
```python
def _lazy_disease():
    global _dis_model, _dis_labels
    if _dis_model is None:
        _dis_model = tf.keras.models.load_model(os.path.join(MODELS_DIR, "disease_model.h5"))
        _dis_labels = ['Healthy', 'Powdery Mildew', 'Rust Disease']
    return _dis_model, _dis_labels
```

## 📊 Model Specifications

### Crop Model
- **Type**: RandomForest Classifier (scikit-learn)
- **Input**: 7 numerical features
- **Output**: 22 crop classes
- **Accuracy**: 99.32%
- **File**: `crop_model.joblib`

### Fertilizer Model
- **Type**: RandomForest Classifier (scikit-learn)
- **Input**: 6 numerical + 2 categorical features (one-hot encoded)
- **Output**: 7 fertilizer types
- **Accuracy**: 100%
- **Files**: `fertilizer_model.joblib`, `fertilizer_model_columns.joblib`

### Disease Model
- **Type**: MobileNetV2 CNN (TensorFlow/Keras)
- **Input**: 224x224x3 RGB images
- **Output**: 3 classes (Healthy, Powdery Mildew, Rust Disease)
- **Architecture**: Transfer learning with fine-tuning
- **File**: `disease_model.h5`

## 🚀 Performance Optimizations

### Lazy Loading Benefits
- **Faster Startup**: Models loaded only when needed
- **Memory Efficient**: Only required models in memory
- **Scalable**: Easy to add new models

### Caching Strategy
```python
# Global variables cache loaded models
# Subsequent calls use cached models
# No repeated file I/O operations
```

### Error Handling
```python
try:
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(df)[0]
        # ... confidence calculation
except:
    pass  # Graceful fallback if confidence unavailable
```

## 🔧 Dependencies

### Core Libraries
```python
import os, io
import numpy as np
from joblib import load
from PIL import Image
import tensorflow as tf
```

### Model Files Required
```
new model/
├── crop_model.joblib
├── fertilizer_model.joblib
├── fertilizer_model_columns.joblib
└── disease_model.h5
```

## 🚨 Error Scenarios

### Missing Model Files
- **Behavior**: Exception raised on first prediction attempt
- **Solution**: Ensure all model files exist in MODELS_DIR

### Invalid Input Data
- **Crop/Fertilizer**: Pandas DataFrame creation may fail
- **Disease**: PIL Image loading may fail
- **Solution**: Input validation in API layer

### Memory Issues
- **Large Models**: TensorFlow model may require significant RAM
- **Solution**: Monitor memory usage, consider model optimization

## 🔍 Usage Examples

### Crop Prediction
```python
from src.inference.predict import predict_crop

features = {
    "N": 90, "P": 42, "K": 43,
    "temperature": 20.87, "humidity": 82.00,
    "ph": 6.50, "rainfall": 202.93
}

result = predict_crop(features)
print(f"Recommended crop: {result['crop']} (confidence: {result['confidence']:.2f})")
```

### Disease Detection
```python
from src.inference.predict import predict_disease

with open("plant_image.jpg", "rb") as f:
    image_bytes = f.read()

result = predict_disease(image_bytes)
print(f"Disease: {result['disease']} (confidence: {result['confidence']:.2f})")
```

---

**File Location**: `/src/inference/predict.py`  
**Type**: Python Module  
**Dependencies**: NumPy, Pandas, Joblib, PIL, TensorFlow  
**Model Files**: 4 files in `new model/` directory  
**Used By**: FastAPI endpoints, prediction services