# KrishiSaathi — Frontend

## Tech Stack
- React 19, Tailwind CSS, Axios, Lucide React
- Served via Nginx (production Docker build)

---

## Architecture

Single Page Application (SPA) with React Router handled by Nginx.
All state is managed locally with React hooks — no Redux or external state library.

---

## Features & How They Work

### 1. Authentication (Login / Register)
- File: `src/components/Login.jsx`
- User fills username, password (and email + language on register)
- POST to `/auth/register` or `/auth/login`
- On login success, JWT token and user object are saved to `localStorage`
- `AuthContext` (`src/context/AuthContext.jsx`) provides `user`, `login`, `logout`, `updateLanguage` globally across the app
- On 401 response anywhere in the app, `api.js` interceptor auto-logs the user out and redirects to login

### 2. Crop Recommendation
- File: `src/App.jsx` — `handleCropSubmit`
- User inputs: Nitrogen (N), Phosphorus (P), Potassium (K), Temperature, Humidity, pH, Rainfall
- POST to `/predict/crop` with JWT in Authorization header
- Response: recommended crop name + confidence score
- Result displayed in the Results panel on the right

### 3. Fertilizer Recommendation
- File: `src/App.jsx` — `handleFertSubmit`
- User inputs: Temperature, Humidity, Moisture, Soil Type (dropdown), Crop Type (dropdown), N, P, K
- POST to `/predict/fertilizer`
- Response: recommended fertilizer name
- Soil types: Sandy, Loamy, Clayey, Black, Red
- Crop types: Rice (Paddy), Wheat, Maize, Sugarcane, Cotton

### 4. Disease Detection
- File: `src/App.jsx` — `handleDiseaseSubmit`
- User uploads a plant/leaf image
- Sent as `multipart/form-data` POST to `/predict/disease`
- Response: disease name, base disease, confidence score, severity level
- Severity logic: Healthy / Early / Moderate / Severe based on confidence threshold

### 5. AI Chatbot
- File: `src/components/ChatBot.jsx`
- Full-screen chat interface with message history persisted in `localStorage`
- Features:
  - Text chat — POST to `/chat` as `multipart/form-data`
  - Image attachment — user can attach a plant photo for AI visual analysis
  - Voice input — Web Speech API (`webkitSpeechRecognition`) for speech-to-text
  - Voice output — Web Speech Synthesis API reads bot responses aloud
  - Language selector — 10 Indian languages supported
  - Clear chat button
- Stale closure fix: `sendMessageRef` keeps speech recognition's `onresult` handler pointing to the latest `sendMessage` function

### 6. Multi-language Support
- File: `src/components/TranslatedText.jsx`
- Calls Google Translate free endpoint client-side to translate UI text
- Language preference saved per user in MongoDB and in `localStorage`
- Language can be changed from the header dropdown — updates backend via `PUT /auth/language`

### 7. Responsive Design
- Tailwind CSS utility classes
- Mobile: hamburger menu with dropdown for Chat, Language, Logout
- Desktop: inline header controls
- Sticky floating chat button (bottom-right) on all screen sizes

---

## API Communication
- File: `src/services/api.js`
- Axios instance with base URL from `REACT_APP_API_BASE_URL` env variable
- Request interceptor: attaches `Authorization: Bearer <token>` to every request
- Response interceptor: on 401, clears localStorage and redirects to login

---

## Build & Deployment
- Development: `npm run dev` (react-scripts on port 3000)
- Production: multi-stage Docker build
  - Stage 1 (builder): Node 20 Alpine, `npm ci`, `npm run build` → static files
  - Stage 2: Nginx Alpine serves `/app/build` on port 80
  - Nginx config handles React Router with `try_files $uri /index.html`
  - Static assets cached for 1 year with `Cache-Control: public, immutable`
  - Gzip compression enabled for JS, CSS, JSON

---

## Environment Variables
| Variable | Purpose |
|---|---|
| REACT_APP_API_BASE_URL | Backend API base URL |
