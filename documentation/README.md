# 📚 KrishiSaathi Documentation

This directory contains detailed documentation for every file in the KrishiSaathi project. Each file has been analyzed and documented to provide comprehensive understanding of the codebase.

## 📁 Documentation Structure

### Root Level Files
- [config.yaml](./root/config.yaml.md) - Global configuration for training and model parameters
- [database.py](./root/database.py.md) - PostgreSQL database operations and user management
- [languages.py](./root/languages.py.md) - Multi-language support definitions and translations
- [mongo_database.py](./root/mongo_database.py.md) - MongoDB database operations (alternative)
- [translator.py](./root/translator.py.md) - Real-time translation service using Google Translate API
- [requirements.txt](./root/requirements.txt.md) - Python dependencies for the main application
- [requirements_speech.txt](./root/requirements_speech.txt.md) - Speech recognition dependencies
- [requirements_web_speech.txt](./root/requirements_web_speech.txt.md) - Web speech API dependencies
- [netlify.toml](./root/netlify.toml.md) - Netlify deployment configuration
- [Procfile](./root/Procfile.md) - Heroku deployment configuration

### Backend API (`src/api/`)
- [main.py](./src/api/main.py.md) - FastAPI application with all endpoints
- [speech_routes.py](./src/api/speech_routes.py.md) - Speech processing API routes

### Machine Learning (`src/`)
- **Inference**
  - [predict.py](./src/inference/predict.py.md) - ML model prediction functions
- **Training**
  - [train_crop.py](./src/training/train_crop.py.md) - Crop recommendation model training
  - [train_disease.py](./src/training/train_disease.py.md) - Disease detection model training
  - [train_fertilizer.py](./src/training/train_fertilizer.py.md) - Fertilizer recommendation model training
- **Pipelines**
  - [crop_pipeline.py](./src/pipelines/crop_pipeline.py.md) - Crop model training pipeline
  - [disease_pipeline.py](./src/pipelines/disease_pipeline.py.md) - Disease model training pipeline
  - [fert_pipeline.py](./src/pipelines/fert_pipeline.py.md) - Fertilizer model training pipeline
  - [helpers.py](./src/pipelines/helpers.py.md) - Pipeline utility functions
- **Features**
  - [preprocess.py](./src/features/preprocess.py.md) - Data preprocessing utilities

### AI Chatbot (`src/chatbot/`)
- [llama_chatbot_simple.py](./src/chatbot/llama_chatbot_simple.py.md) - Main chatbot implementation
- [data_processor.py](./src/chatbot/data_processor.py.md) - Agricultural data processing
- [kcc_data_fetcher.py](./src/chatbot/kcc_data_fetcher.py.md) - Government data fetching

### Frontend (`frontend/`)
- **Main Application**
  - [App.jsx](./frontend/src/App.jsx.md) - Main React application component
  - [index.js](./frontend/src/index.js.md) - React application entry point
- **Components**
  - [Login.jsx](./frontend/src/components/Login.jsx.md) - User authentication component
  - [ChatBot.jsx](./frontend/src/components/ChatBot.jsx.md) - AI chatbot interface
  - [TranslatedText.jsx](./frontend/src/components/TranslatedText.jsx.md) - Text translation component
  - [ComingSoon.jsx](./frontend/src/components/ComingSoon.jsx.md) - Coming soon features page
  - [SpeechChat.jsx](./frontend/src/components/SpeechChat.jsx.md) - Speech-enabled chat
  - [WebSpeechChat.jsx](./frontend/src/components/WebSpeechChat.jsx.md) - Web Speech API integration
- **Configuration**
  - [package.json](./frontend/package.json.md) - Frontend dependencies and scripts
  - [tailwind.config.js](./frontend/tailwind.config.js.md) - Tailwind CSS configuration
  - [postcss.config.js](./frontend/postcss.config.js.md) - PostCSS configuration

### Models (`new model/`)
- [crop_model.joblib](./models/crop_model.joblib.md) - Trained crop recommendation model
- [disease_model.h5](./models/disease_model.h5.md) - Trained disease detection model
- [fertilizer_model.joblib](./models/fertilizer_model.joblib.md) - Trained fertilizer recommendation model
- [fertilizer_model_columns.joblib](./models/fertilizer_model_columns.joblib.md) - Fertilizer model feature columns

## 🎯 Quick Navigation

### For Developers
- **Getting Started**: See [main README](../README.md)
- **API Documentation**: [main.py](./src/api/main.py.md)
- **Model Training**: [Training Scripts](./src/training/)
- **Frontend Setup**: [package.json](./frontend/package.json.md)

### For Data Scientists
- **Model Architecture**: [Pipeline Documentation](./src/pipelines/)
- **Data Processing**: [preprocess.py](./src/features/preprocess.py.md)
- **Model Inference**: [predict.py](./src/inference/predict.py.md)

### For DevOps
- **Deployment**: [netlify.toml](./root/netlify.toml.md), [Procfile](./root/Procfile.md)
- **Dependencies**: [requirements.txt](./root/requirements.txt.md)
- **Configuration**: [config.yaml](./root/config.yaml.md)

## 📊 Project Statistics

- **Total Files Documented**: 50+
- **Programming Languages**: Python, JavaScript, YAML, JSON
- **Frameworks**: FastAPI, React, TensorFlow, Scikit-learn
- **Database Support**: PostgreSQL, MongoDB
- **AI Models**: 3 (Crop, Fertilizer, Disease)
- **Languages Supported**: 26 Indian languages

## 🔍 Search Tips

Use Ctrl+F to search for:
- Specific file names
- Technology keywords (FastAPI, React, TensorFlow)
- Feature names (crop recommendation, disease detection)
- Configuration parameters

---

*This documentation was automatically generated to provide comprehensive coverage of the KrishiSaathi codebase.*