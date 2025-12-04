# src/training/train_crop.py

## 📋 Overview
Training script for the crop recommendation model using RandomForest classifier. Supports both real agricultural datasets and synthetic data generation for testing and development.

## 🎯 Purpose
- Train machine learning model for crop recommendations
- Support multiple data sources (real datasets or synthetic data)
- Implement configurable hyperparameters via YAML config
- Provide model evaluation and persistence
- Enable reproducible training with fixed random seeds

## 🏗️ Script Architecture

### Main Components
```python
def load_config()                    # Load YAML configuration
def make_synthetic(n=500)           # Generate synthetic training data
def main()                          # Main training pipeline
```

## ⚙️ Configuration Management

### YAML Config Loading
```python
def load_config():
    with open("config.yaml","r") as f:
        return yaml.safe_load(f)
```

**Configuration Structure**:
```yaml
crop:
  csv_path: data/raw/crop_recommendation/crop_recommendation.csv
  target: label
  test_size: 0.2
  rf_params:
    n_estimators: 300
    max_depth: null
    n_jobs: -1
```

## 🔬 Synthetic Data Generation

### Data Generation Function
```python
def make_synthetic(n=500):
    rng = np.random.default_rng(42)  # Fixed seed for reproducibility
    df = pd.DataFrame({
        "N": rng.integers(0,140,n),           # Nitrogen: 0-140 kg/ha
        "P": rng.integers(0,140,n),           # Phosphorus: 0-140 kg/ha
        "K": rng.integers(0,200,n),           # Potassium: 0-200 kg/ha
        "temperature": rng.normal(25,6,n).round(2),    # Temperature: ~25°C ±6
        "humidity": rng.uniform(20,95,n).round(2),     # Humidity: 20-95%
        "ph": rng.uniform(4.0,8.5,n).round(2),        # pH: 4.0-8.5
        "rainfall": rng.uniform(10,300,n).round(2),    # Rainfall: 10-300mm
    })
    
    # Rule-based label generation
    labels = np.where((df["N"]>80)&(df["P"]>60)&(df["K"]>60)&(df["rainfall"]>150), "rice",
             np.where(df["temperature"]<22, "wheat", "maize"))
    df["label"] = labels
    return df
```

### Synthetic Data Rules
1. **Rice**: High NPK (>80, >60, >60) + High rainfall (>150mm)
2. **Wheat**: Low temperature (<22°C)
3. **Maize**: Default for other conditions

## 🚀 Training Pipeline

### Main Training Function
```python
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--synthetic", action="store_true", help="use synthetic data")
    args = ap.parse_args()
    
    cfg = load_config()
    
    # Data loading
    if args.synthetic:
        df = make_synthetic()
    else:
        csv = cfg["crop"]["csv_path"]
        if not os.path.exists(csv):
            raise FileNotFoundError(f"Expected CSV at {csv}. Use --synthetic to test.")
        df = pd.read_csv(csv)
    
    # Model training
    pipe, acc = train_crop_model(df, cfg)
    
    # Model persistence
    os.makedirs(cfg["models_dir"], exist_ok=True)
    out = os.path.join(cfg["models_dir"], "crop_rf.joblib")
    dump(pipe, out)
    
    print(f"Crop model saved to {out}. Test accuracy ~ {acc:.3f}")
```

## 📊 Feature Engineering

### Input Features (7 features)
1. **N** (Nitrogen): Soil nitrogen content (kg/ha)
2. **P** (Phosphorus): Soil phosphorus content (kg/ha)
3. **K** (Potassium): Soil potassium content (kg/ha)
4. **temperature**: Average temperature (°C)
5. **humidity**: Relative humidity (%)
6. **ph**: Soil pH level (4.0-8.5)
7. **rainfall**: Annual rainfall (mm)

### Target Variable
- **label**: Crop type (rice, wheat, maize, cotton, etc.)

## 🤖 Model Architecture

### RandomForest Configuration
```python
# From config.yaml
rf_params:
  n_estimators: 300    # Number of decision trees
  max_depth: null      # No depth limit (full trees)
  n_jobs: -1          # Use all CPU cores
```

### Pipeline Structure
```python
# From crop_pipeline.py
pipe = Pipeline(steps=[
    ("prep", preprocessor),     # Data preprocessing
    ("clf", RandomForestClassifier(**rf_params))  # Classification
])
```

## 📈 Model Performance

### Expected Accuracy
- **Real Dataset**: ~99.32% (as reported in main README)
- **Synthetic Dataset**: Variable (depends on rule complexity)

### Evaluation Metrics
- **Test Accuracy**: Primary metric
- **Cross-validation**: Available through pipeline
- **Feature Importance**: Available from RandomForest

## 🔧 Usage Examples

### Training with Real Data
```bash
python src/training/train_crop.py
```

**Requirements**:
- CSV file at `data/raw/crop_recommendation/crop_recommendation.csv`
- Proper column names matching config

### Training with Synthetic Data
```bash
python src/training/train_crop.py --synthetic
```

**Benefits**:
- No external dataset required
- Quick testing and development
- Reproducible results

### Custom Configuration
```bash
# Modify config.yaml first
crop:
  rf_params:
    n_estimators: 500    # More trees for better accuracy
    max_depth: 20        # Limit depth to prevent overfitting
```

## 📁 File Dependencies

### Required Files
```
config.yaml                           # Configuration file
src/pipelines/crop_pipeline.py       # Training pipeline
src/features/preprocess.py           # Data preprocessing
```

### Optional Files
```
data/raw/crop_recommendation/crop_recommendation.csv  # Real dataset
```

### Output Files
```
models/crop_rf.joblib                # Trained model (configurable path)
```

## 🔍 Data Validation

### Real Dataset Requirements
```python
# Expected columns in CSV
required_columns = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall", "label"]

# Data types
numeric_features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
categorical_target = "label"
```

### Data Quality Checks
- **Missing Values**: Handle NaN values in preprocessing
- **Outliers**: RandomForest is robust to outliers
- **Feature Scaling**: Handled in preprocessing pipeline
- **Class Balance**: Check target distribution

## 🚨 Error Handling

### Common Errors
1. **FileNotFoundError**: CSV file not found
   ```python
   if not os.path.exists(csv):
       raise FileNotFoundError(f"Expected CSV at {csv}. Use --synthetic to test.")
   ```

2. **Configuration Errors**: Invalid YAML format
3. **Memory Errors**: Large datasets with many trees
4. **Import Errors**: Missing dependencies

### Debugging Tips
```python
# Add debug prints
print(f"Dataset shape: {df.shape}")
print(f"Target distribution: {df['label'].value_counts()}")
print(f"Feature columns: {df.columns.tolist()}")
```

## 🔄 Model Versioning

### Model Persistence
```python
from joblib import dump
dump(pipe, "models/crop_rf.joblib")
```

### Version Control
- **Git**: Track training scripts and configs
- **Model Registry**: Consider MLflow or similar
- **Experiment Tracking**: Log hyperparameters and metrics

## 📊 Hyperparameter Tuning

### Grid Search Example
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'clf__n_estimators': [100, 200, 300],
    'clf__max_depth': [None, 10, 20, 30],
    'clf__min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(pipe, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
```

### Random Search Alternative
```python
from sklearn.model_selection import RandomizedSearchCV

param_dist = {
    'clf__n_estimators': [100, 200, 300, 400, 500],
    'clf__max_depth': [None, 5, 10, 15, 20, 25, 30],
    'clf__min_samples_split': [2, 5, 10, 15, 20]
}

random_search = RandomizedSearchCV(pipe, param_dist, n_iter=20, cv=5, scoring='accuracy')
```

## 🚀 Production Deployment

### Model Validation
```python
# Validate model before deployment
assert pipe.score(X_test, y_test) > 0.95, "Model accuracy too low"
assert len(pipe.classes_) > 10, "Too few crop classes"
```

### Model Monitoring
- **Accuracy Tracking**: Monitor prediction accuracy over time
- **Data Drift**: Detect changes in input feature distributions
- **Performance Metrics**: Track inference time and memory usage

---

**File Location**: `/src/training/train_crop.py`  
**Type**: Python Training Script  
**Dependencies**: pandas, numpy, scikit-learn, joblib, PyYAML  
**Input**: CSV dataset or synthetic data  
**Output**: Trained RandomForest model (joblib format)  
**Accuracy**: 99.32% on real agricultural dataset