from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017/krishisaathi"
    JWT_SECRET_KEY: str = "change_this_in_production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    GEMINI_API_KEY: str = ""
    GROK_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""

    OPENWEATHER_API_KEY: str = ""

    MODELS_DIR: str = "models/ml_models"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
