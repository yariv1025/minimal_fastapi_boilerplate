import os

from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Application settings using environment variables.
    """

    # App
    app_version: str = os.getenv("APP_VERSION")
    host: str = os.getenv("HOST")
    port: int = os.getenv("PORT")
    workers: int = os.getenv("WORKERS")
    log_level: str = os.getenv("LOG_LEVEL")
    reload: bool = os.getenv("RELOAD")


    # Mongo
    MONGO_ADMIN_USER: str = os.getenv("MONGO_ADMIN_USER")
    MONGO_ADMIN_PASSWORD: str = os.getenv("MONGO_ADMIN_PASSWORD")
    MONGO_DOMAIN: str = os.getenv("MONGO_DOMAIN")
    MONGO_PORT: str = os.getenv("MONGO_PORT")
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")
    MONGO_COLLECTION_NAME: str = os.getenv("MONGO_COLLECTION_NAME")


    class Config:
        env_file = "../../.env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
