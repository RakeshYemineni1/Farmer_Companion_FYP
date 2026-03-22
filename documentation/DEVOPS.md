# KrishiSaathi — DevOps & Docker

## Overview

KrishiSaathi runs as 3 Docker containers orchestrated with Docker Compose:
- mongo — MongoDB database
- backend — FastAPI Python server
- frontend — React app served by Nginx

---

## Container Architecture

```
┌─────────────────────────────────────────────┐
│              Docker Network                  │
│                                             │
│  ┌──────────┐    ┌──────────┐    ┌────────┐ │
│  │ frontend │───▶│ backend  │───▶│ mongo  │ │
│  │  :3000   │    │  :8000   │    │ :27017 │ │
│  │  Nginx   │    │ FastAPI  │    │MongoDB │ │
│  └──────────┘    └──────────┘    └────────┘ │
└─────────────────────────────────────────────┘
         ▲                ▲
    Browser           External APIs
                   (Gemini, OpenWeather)
```

---

## Docker Compose (`docker-compose.yml`)

### mongo service
- Image: `mongo:7` (official)
- Named volume `mongo_data` for persistent storage
- Healthcheck: `mongosh --eval "db.adminCommand('ping')"` every 10s
- Backend waits for mongo to be healthy before starting (`depends_on: condition: service_healthy`)

### backend service
- Built from `./backend/Dockerfile`
- Reads all secrets from `.env` file via `env_file`
- Port 8000 exposed to host
- Healthcheck: `curl -f http://localhost:8000/health` every 30s
- Restarts automatically unless manually stopped

### frontend service
- Built from `./frontend/Dockerfile`
- Build arg `REACT_APP_API_BASE_URL` passed at build time (baked into JS bundle)
- Port 3000 on host → port 80 in container (Nginx)
- Depends on backend being up

---

## Backend Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get install curl libgomp1 libglib2.0-0 libsm6 libxext6
COPY requirements.txt .
RUN pip install -r requirements.txt        # cached layer
COPY . ./backend                           # source copied last
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Key decisions:
- `python:3.11-slim` — minimal base image, reduces size
- `libgomp1` — required by scikit-learn for parallel processing
- `libglib2.0-0`, `libsm6`, `libxext6` — required by OpenCV/TensorFlow
- requirements copied and installed before source code — Docker layer cache means pip only re-runs when requirements.txt changes, not on every code change
- `--mount=type=cache` on pip install — speeds up rebuilds by caching downloaded packages
- Source copied to `./backend` so Python imports work as `from backend.xxx import ...`
- Uvicorn runs with `0.0.0.0` to accept connections from outside the container

---

## Frontend Dockerfile (Multi-stage)

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci                    # clean install, faster than npm install
COPY . .
ARG REACT_APP_API_BASE_URL
ENV REACT_APP_API_BASE_URL=$REACT_APP_API_BASE_URL
RUN npm run build             # outputs to /app/build

# Stage 2: Serve
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

Key decisions:
- Multi-stage build — Node.js (400MB+) is only used to build, final image is just Nginx Alpine (~25MB)
- `npm ci` instead of `npm install` — faster, deterministic, uses package-lock.json exactly
- `REACT_APP_API_BASE_URL` baked in at build time — React env vars must be available during `npm run build`
- Nginx serves static files, handles React Router with `try_files $uri /index.html`

---

## Nginx Configuration

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;

    location / {
        try_files $uri $uri/ /index.html;   # React Router support
    }

    location ~* \.(js|css|png|jpg|ico|svg|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";  # aggressive caching
    }

    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
}
```

- `try_files` — prevents 404 on page refresh for React routes like `/chat`
- 1 year cache on static assets — React build adds content hash to filenames so cache busting is automatic
- Gzip compression reduces JS/CSS transfer size by ~70%

---

## Dependency & Startup Order

```
mongo (starts) → healthcheck passes → backend (starts) → frontend (starts)
```

- If mongo is not ready, backend won't start (Motor connection would fail)
- Backend has its own healthcheck so load balancers/orchestrators can detect crashes
- `restart: unless-stopped` on all services — auto-recover from crashes

---

## Key Pinned Versions (requirements.txt)

| Package | Version | Reason |
|---|---|---|
| motor | 3.6.0 | Async MongoDB driver |
| pymongo | 4.9.2 | motor 3.6 requires pymongo >=4.9, <4.10 |
| bcrypt | 4.0.1 | passlib 1.7.4 incompatible with bcrypt 5.x |
| tensorflow-cpu | 2.16.1 | CPU-only build, no GPU needed |
| scikit-learn | 1.5.0 | Must match version used to train models |

---

## How to Run

```bash
# Clone and configure
git clone https://github.com/prathyush04/KrishiSaathi.git
cd KrishiSaathi

# Add your API keys to .env
# GEMINI_API_KEY, GROK_API_KEY, OPENROUTER_API_KEY = your 3 Gemini keys

# Start everything
docker compose up --build -d

# Check status
docker compose ps

# View logs
docker logs krishisaathi_backend
docker logs krishisaathi_frontend
docker logs krishisaathi_mongo

# Stop
docker compose down

# Stop and delete database
docker compose down -v
```

---

## URLs
| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |
| MongoDB | mongodb://localhost:27017 |

---

## Production Deployment Notes
- Frontend deployed to Netlify (static hosting) — `netlify.toml` configured
- Backend deployed to any Docker-compatible host (Railway, Render, EC2, etc.)
- Set `REACT_APP_API_BASE_URL` to production backend URL at build time
- Add production frontend URL to CORS `allow_origins` in `backend/main.py`
- Replace `JWT_SECRET_KEY` with a strong random secret in production `.env`
