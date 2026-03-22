# KrishiSaathi — Backend

## Tech Stack
- FastAPI (Python 3.11)
- MongoDB (async via Motor)
- TensorFlow/Keras — disease detection
- Scikit-learn — crop & fertilizer prediction
- Google Gemini API — AI chatbot
- JWT (python-jose) — authentication
- Passlib + bcrypt — password hashing
- Httpx — async HTTP client

---

## Project Structure

```
backend/
├── main.py                  # App entry point, CORS, routers
├── languages.py             # Language list + translation cache
├── api/routes/
│   ├── auth_routes.py       # Register, login, language update
│   ├── prediction_routes.py # Crop, fertilizer, disease endpoints
│   ├── chat_routes.py       # Chat + speech + history
│   └── weather_routes.py    # Weather forecast + farming advisory
├── core/
│   ├── config.py            # Pydantic settings from .env
│   ├── security.py          # JWT create/decode, bcrypt hash/verify
│   └── dependencies.py      # get_current_user JWT guard
├── db/
│   └── mongo_database.py    # Motor async MongoDB client
├── models/
│   ├── ml_models/           # .joblib and .h5 model files
│   └── chat_models/
│       └── gemini_client.py # Gemini API client
├── services/
│   ├── prediction_service.py
│   ├── chat_service.py
│   └── weather_service.py
└── utils/
    ├── fallback_router.py   # Multi-key Gemini fallback logic
    └── translation.py       # Google Translate async utility
```

---

## Features & How They Work

### 1. Authentication

**Register** — `POST /auth/register`
- Accepts username, email, password, language
- Checks for duplicate username/email in MongoDB
- Hashes password with bcrypt (passlib)
- Stores user document in `users` collection

**Login** — `POST /auth/login`
- Verifies password against stored bcrypt hash
- Returns JWT token (expires in 1440 min / 24 hours)
- JWT payload contains `sub` (username) and `language`

**JWT Guard** — `core/dependencies.py`
- `get_current_user` dependency used on all protected routes
- Extracts Bearer token from Authorization header
- Decodes and validates JWT, returns payload dict
- Raises 401 on invalid or expired token

**Language Update** — `PUT /auth/language`
- Protected by JWT — users can only update their own language
- Updates `language` field in MongoDB users collection

---

### 2. Crop Recommendation

**Endpoint** — `POST /predict/crop`

**Input:** N, P, K, temperature, humidity, ph, rainfall

**Model:** RandomForest Classifier (`crop_model.joblib`)
- Trained on agricultural dataset with 22 crop classes
- Accuracy: 99.32%

**Implementation** (`prediction_service.py`):
- Lazy-loaded on first request to avoid startup delay
- Input converted to pandas DataFrame
- `predict()` returns crop name
- `predict_proba()` returns confidence score
- Result + inputs saved to `crop_predictions` collection in MongoDB

---

### 3. Fertilizer Recommendation

**Endpoint** — `POST /predict/fertilizer`

**Input:** temperature, humidity, moisture, soil_type, crop_type, N, P, K

**Model:** RandomForest Classifier (`fertilizer_model.joblib`)
- 7 fertilizer classes (Urea, DAP, 10-26-26, etc.)
- Accuracy: 100%

**Implementation:**
- Categorical features (soil_type, crop_type) are one-hot encoded manually to match training columns
- Supported soil types: Sandy, Loamy, Clayey, Black, Red
- Supported crop types: Cotton, Ground Nuts, Maize, Millets, Oil seeds, Paddy, Pulses, Sugarcane, Tobacco, Wheat
- Column order enforced via `fertilizer_model_columns.joblib`
- Result saved to `fertilizer_predictions` collection

---

### 4. Disease Detection

**Endpoint** — `POST /predict/disease`

**Input:** plant image (multipart upload)

**Model:** MobileNetV2 CNN (`disease_model.h5`)
- Input: 224x224 RGB image
- 3 output classes: Healthy, Powdery Mildew, Rust Disease
- Framework: TensorFlow/Keras

**Implementation:**
- Image bytes decoded with Pillow, resized to 224x224, normalized to 0-1
- Model predicts probability for each class
- Severity logic based on confidence:
  - >= 0.85 → Early stage
  - >= 0.65 → Moderate
  - < 0.65 → Severe
- Result saved to `disease_predictions` collection

---

### 5. AI Chatbot

**Endpoints:**
- `POST /chat` — text + optional image (multipart)
- `POST /chat/speech` — transcribed speech text
- `GET /chat/history` — last 20 messages for the user

**Flow** (`chat_service.py`):
1. Message received with language code
2. Passed directly to `ChatFallbackRouter.get_response(message, image, language)`
3. Gemini responds directly in the target language (no translation layer)
4. Response stripped of markdown server-side
5. Conversation saved to `chat_history` collection

**Fallback Router** (`utils/fallback_router.py`):
- 3 Gemini API keys configured (GEMINI_API_KEY, GROK_API_KEY, OPENROUTER_API_KEY)
- Each key paired with a different model: gemini-2.0-flash, gemini-2.5-flash, gemini-2.5-flash-lite
- Tries key 1 first — if it fails or is exhausted, automatically tries key 2, then key 3
- 30 second timeout per provider
- Markdown stripping via regex on all responses

**System Prompt:**
- Instructs Gemini to act as a friendly farming assistant
- No markdown or special characters
- For images: identify crop, detect disease/pest, assess severity, give treatment
- Always respond in the user's selected language

**Gemini Client** (`models/chat_models/gemini_client.py`):
- For text: system prompt + user message in one part
- For images: system prompt + base64 encoded image + analysis instruction
- Uses Gemini's `generateContent` REST API

---

### 6. Weather & Farming Advisory

**Endpoint** — `GET /weather/forecast?lat=&lon=`

**Implementation** (`weather_service.py`):
- Calls OpenWeatherMap forecast API (7 data points)
- For each forecast entry, evaluates 6 farming advisory rules:
  - Humidity > 80% → fungal disease warning
  - Rain > 20mm → delay fertilizer application
  - Hot + dry → irrigation recommended
  - Wind > 40 km/h → avoid pesticide spraying
  - Temp < 10°C → frost protection warning
  - Moderate rain → good sowing conditions
- Returns location name, forecast array with advisories
- Saved to `weather_history` collection

---

### 7. Multi-language Translations

**Endpoint** — `GET /translations/{language}`

**Implementation** (`languages.py`):
- Static translations for English, Hindi, Bengali, Tamil (fast, no API call)
- All other languages: batch translated via Google Translate free endpoint
- Results cached in-memory to avoid repeated API calls
- 15 Indian languages supported

---

## Database (MongoDB)

Collections:
| Collection | Purpose |
|---|---|
| users | User accounts |
| crop_predictions | Crop prediction history |
| fertilizer_predictions | Fertilizer prediction history |
| disease_predictions | Disease detection history |
| chat_history | Chatbot conversation history |
| weather_history | Weather forecast history |

Indexes:
- `users.username` — unique
- `users.email` — unique

---

## Security
- Passwords hashed with bcrypt (cost factor default)
- JWT signed with HS256, configurable secret key
- All prediction and chat endpoints require valid JWT
- CORS restricted to localhost:3000 and production Netlify URL
- API keys stored in .env, never in code

---

## Environment Variables
| Variable | Purpose |
|---|---|
| MONGODB_URL | MongoDB connection string |
| JWT_SECRET_KEY | JWT signing secret |
| JWT_EXPIRE_MINUTES | Token expiry (default 1440) |
| GEMINI_API_KEY | Gemini key 1 (gemini-2.0-flash) |
| GROK_API_KEY | Gemini key 2 (gemini-2.5-flash) |
| OPENROUTER_API_KEY | Gemini key 3 (gemini-2.5-flash-lite) |
| OPENWEATHER_API_KEY | OpenWeatherMap API key |
| MODELS_DIR | Path to ML model files |
