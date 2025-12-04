# requirements.txt

## 📋 Overview
Main Python dependencies file that defines all required packages for the KrishiSaathi backend application, including machine learning, web framework, database, and AI chatbot dependencies.

## 🎯 Purpose
- Define exact package versions for reproducible deployments
- Organize dependencies by functional categories
- Ensure compatibility across different environments
- Support both development and production deployments

## 📦 Dependency Categories

### Core Data Science Libraries
```txt
numpy                    # Numerical computing foundation
pandas                   # Data manipulation and analysis
scikit-learn            # Machine learning algorithms
joblib                  # Model serialization and parallel processing
pydantic                # Data validation and settings management
pyyaml                  # YAML configuration file parsing
```

**Purpose**:
- **NumPy**: Array operations, mathematical functions
- **Pandas**: CSV loading, data preprocessing, feature engineering
- **Scikit-learn**: RandomForest models, preprocessing pipelines
- **Joblib**: Efficient model saving/loading, parallel processing
- **Pydantic**: API request/response validation, type checking
- **PyYAML**: Configuration file management

### Web Framework & API
```txt
fastapi                 # Modern Python web framework
uvicorn                 # ASGI server for FastAPI
python-multipart        # File upload support
```

**Features**:
- **FastAPI**: Automatic API documentation, type hints, async support
- **Uvicorn**: High-performance ASGI server with hot reload
- **Python-multipart**: Handle image uploads for disease detection

### Deep Learning & Computer Vision
```txt
tensorflow              # Deep learning framework
pillow                  # Image processing library
```

**Applications**:
- **TensorFlow**: MobileNetV2 disease detection model
- **Pillow**: Image preprocessing, format conversion, resizing

### Visualization & Analysis
```txt
matplotlib              # Plotting and visualization
```

**Usage**:
- Model performance visualization
- Data exploration plots
- Training metrics visualization
- Optional for production deployment

### Database Support
```txt
pymongo                 # MongoDB driver
```

**Features**:
- NoSQL database operations
- User data storage
- Alternative to PostgreSQL
- Flexible document storage

### AI Chatbot Dependencies
```txt
nltk                    # Natural language processing
sentence-transformers   # Semantic text embeddings
requests                # HTTP client for external APIs
```

**Chatbot Features**:
- **NLTK**: Text preprocessing, tokenization
- **Sentence-transformers**: Semantic similarity search
- **Requests**: Translation API calls, data fetching

### Advanced AI Models
```txt
transformers            # Hugging Face transformers library
torch                   # PyTorch deep learning framework
datasets                # Dataset loading and processing
accelerate              # Distributed training acceleration
bitsandbytes           # Model quantization and optimization
```

**LLaMA Integration**:
- **Transformers**: Pre-trained language models
- **PyTorch**: Neural network backend
- **Datasets**: Agricultural dataset management
- **Accelerate**: Multi-GPU training support
- **BitsAndBytes**: Memory-efficient model loading

## 🔧 Installation Instructions

### Standard Installation
```bash
pip install -r requirements.txt
```

### Virtual Environment (Recommended)
```bash
python -m venv krishisaathi_env
source krishisaathi_env/bin/activate  # Linux/Mac
# or
krishisaathi_env\Scripts\activate     # Windows

pip install -r requirements.txt
```

### Docker Installation
```dockerfile
FROM python:3.8-slim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

## 📊 Package Analysis

### Core Dependencies (Always Required)
- **FastAPI Stack**: Web framework and server
- **ML Stack**: NumPy, Pandas, Scikit-learn
- **Config Management**: PyYAML, Pydantic

### Optional Dependencies
- **TensorFlow**: Only if using disease detection
- **MongoDB**: Only if using MongoDB instead of PostgreSQL
- **Matplotlib**: Only for development/analysis
- **LLaMA Stack**: Only for advanced chatbot features

### Lightweight Installation
```txt
# Minimal requirements for basic functionality
numpy
pandas
scikit-learn
joblib
fastapi
uvicorn
pydantic
pyyaml
```

## 🚀 Performance Considerations

### Memory Usage
- **TensorFlow**: ~500MB-1GB RAM
- **Transformers**: ~1-4GB RAM (model dependent)
- **Scikit-learn**: ~50-100MB RAM
- **FastAPI**: ~20-50MB RAM

### Installation Time
- **Full Installation**: 5-15 minutes
- **Core Only**: 1-3 minutes
- **With GPU Support**: 10-30 minutes

### Disk Space
- **Full Installation**: ~2-5GB
- **Core Dependencies**: ~500MB-1GB
- **Model Files**: Additional 1-2GB

## 🔄 Version Management

### Pinning Versions (Production)
```txt
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.0
fastapi==0.100.0
tensorflow==2.13.0
```

### Flexible Versions (Development)
```txt
numpy>=1.20.0
pandas>=1.5.0
scikit-learn>=1.2.0
fastapi>=0.95.0
tensorflow>=2.10.0
```

## 🌍 Environment-Specific Requirements

### Development Environment
```txt
# Additional dev dependencies
pytest                  # Testing framework
black                   # Code formatting
flake8                  # Code linting
jupyter                 # Interactive notebooks
```

### Production Environment
```txt
# Production optimizations
gunicorn               # Production WSGI server
psycopg2-binary       # PostgreSQL adapter
redis                 # Caching layer
```

### GPU Environment
```txt
# GPU-accelerated versions
tensorflow-gpu         # GPU-enabled TensorFlow
torch-gpu             # GPU-enabled PyTorch
```

## 🚨 Common Installation Issues

### TensorFlow Issues
```bash
# CPU-only installation
pip install tensorflow-cpu

# Apple Silicon Macs
pip install tensorflow-macos tensorflow-metal
```

### PyTorch Issues
```bash
# CPU-only installation
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Compilation Issues
```bash
# Install build tools (Ubuntu/Debian)
sudo apt-get install build-essential python3-dev

# Install build tools (CentOS/RHEL)
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel
```

## 🔍 Dependency Conflicts

### Common Conflicts
1. **TensorFlow vs PyTorch**: Different CUDA versions
2. **NumPy versions**: Compatibility with other packages
3. **Protobuf versions**: TensorFlow compatibility issues

### Resolution Strategies
```bash
# Check for conflicts
pip check

# Update conflicting packages
pip install --upgrade numpy tensorflow

# Use conda for complex environments
conda install tensorflow pytorch -c conda-forge
```

## 📈 Optimization Tips

### Faster Installation
```bash
# Use pip cache
pip install --cache-dir ~/.pip/cache -r requirements.txt

# Parallel installation
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --use-pep517
```

### Reduced Size Installation
```bash
# Skip unnecessary dependencies
pip install --no-deps package_name

# Use slim versions
pip install tensorflow-cpu  # Instead of full tensorflow
```

## 🔐 Security Considerations

### Vulnerability Scanning
```bash
# Check for known vulnerabilities
pip audit

# Update vulnerable packages
pip install --upgrade package_name
```

### Trusted Sources
```bash
# Use trusted PyPI index
pip install --index-url https://pypi.org/simple/ -r requirements.txt

# Verify package integrity
pip install --require-hashes -r requirements.txt
```

## 📊 Alternative Package Managers

### Conda Environment
```yaml
# environment.yml
name: krishisaathi
dependencies:
  - python=3.8
  - numpy
  - pandas
  - scikit-learn
  - pip
  - pip:
    - fastapi
    - uvicorn
```

### Poetry Configuration
```toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.8"
numpy = "^1.20.0"
pandas = "^1.5.0"
scikit-learn = "^1.2.0"
fastapi = "^0.95.0"
```

---

**File Location**: `/requirements.txt`  
**Type**: Python Dependencies File  
**Total Packages**: 15+ core dependencies  
**Installation Time**: 5-15 minutes  
**Disk Space**: 2-5GB (full installation)  
**Python Version**: 3.8+ required