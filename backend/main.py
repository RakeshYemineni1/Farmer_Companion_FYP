from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.db.mongo_database import connect_db, close_db
from backend.api.routes import auth_routes, prediction_routes, chat_routes, weather_routes
from backend.languages import INDIAN_LANGUAGES, get_translations


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(title="KrishiSaathi API", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://krishisaathiii.netlify.app",
        "https://68c2c0ec765ff80008709c8a--krishisaathiii.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(prediction_routes.router)
app.include_router(chat_routes.router)
app.include_router(weather_routes.router)


@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}


@app.get("/languages")
def languages():
    return INDIAN_LANGUAGES


@app.get("/translations/{language}")
def translations(language: str):
    return get_translations(language)
