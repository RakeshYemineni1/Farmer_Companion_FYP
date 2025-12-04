# config.yaml

## 📋 Overview
Global configuration file that defines training parameters, model settings, and data paths for all machine learning models in the KrishiSaathi project.

## 🎯 Purpose
- Centralized configuration management for ML pipelines
- Standardized hyperparameters across different models
- Easy modification of training settings without code changes
- Consistent data paths and model directories

## 📊 Configuration Structure

### Global Settings
```yaml
seed: 42                    # Random seed for reproducibility
models_dir: models         # Directory to save trained models
```

### Crop Recommendation Model
```yaml
crop:
  csv_path: data/raw/crop_recommendation/crop_recommendation.csv
  target: label            # Target column name
  test_size: 0.2          # 20% data for testing
  rf_params:              # RandomForest parameters
    n_estimators: 300     # Number of trees
    max_depth: null       # No depth limit
    n_jobs: -1           # Use all CPU cores
```

### Fertilizer Recommendation Model
```yaml
fertilizer:
  csv_path: data/raw/fertilizer_recommendation/fertilizer.csv
  target: Fertilizer Name  # Target column name
  test_size: 0.2          # 20% data for testing
  rf_params:              # RandomForest parameters
    n_estimators: 300     # Number of trees
    max_depth: null       # No depth limit
    n_jobs: -1           # Use all CPU cores
```

### Disease Detection Model
```yaml
disease:
  data_dir: data/raw/plant_disease    # Image dataset directory
  img_size: [224, 224]               # Input image dimensions
  batch_size: 32                     # Training batch size
  epochs: 10                         # Training epochs
  base_trainable_layers: 20          # Fine-tune last 20 layers of MobileNetV2
```

## 🔧 Usage

### In Training Scripts
```python
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()
crop_params = config["crop"]["rf_params"]
```

### Model Directory Creation
```python
import os
os.makedirs(config["models_dir"], exist_ok=True)
```

## 🎛️ Customization Options

### Adjusting Model Performance
- **n_estimators**: Increase for better accuracy (slower training)
- **max_depth**: Set limit to prevent overfitting
- **test_size**: Adjust train/test split ratio

### Image Model Tuning
- **img_size**: Change input resolution (higher = more detail, slower)
- **batch_size**: Adjust based on GPU memory
- **epochs**: Increase for better convergence
- **base_trainable_layers**: More layers = more fine-tuning

## 📁 Data Path Requirements

### Expected Directory Structure
```
data/
├── raw/
│   ├── crop_recommendation/
│   │   └── crop_recommendation.csv
│   ├── fertilizer_recommendation/
│   │   └── fertilizer.csv
│   └── plant_disease/
│       ├── Train/
│       └── Validation/
```

## ⚙️ Model Parameters Explained

### RandomForest Parameters
- **n_estimators**: Number of decision trees in the forest
- **max_depth**: Maximum depth of trees (null = unlimited)
- **n_jobs**: Number of CPU cores to use (-1 = all available)

### CNN Parameters
- **img_size**: Input image dimensions for MobileNetV2
- **batch_size**: Number of images processed simultaneously
- **epochs**: Complete passes through the training data
- **base_trainable_layers**: Number of layers to fine-tune from pre-trained model

## 🔄 Version Control
- Keep this file in version control
- Document changes when modifying parameters
- Test thoroughly after parameter changes

## 🚀 Performance Tips
- Use `n_jobs: -1` for faster training on multi-core systems
- Adjust `batch_size` based on available GPU memory
- Start with default parameters, then optimize based on results

## 📈 Monitoring
- Track model performance metrics after parameter changes
- Use validation accuracy to guide hyperparameter tuning
- Consider cross-validation for robust parameter selection

---

**File Location**: `/config.yaml`  
**Type**: YAML Configuration  
**Dependencies**: PyYAML  
**Used By**: All training scripts, model pipelines