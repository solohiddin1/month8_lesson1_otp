from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# load_dotenv()

class Settings(BaseSettings):
    PHOTO_PATH: str 
    DEFAULT_PHOTO_PATH: str 
    VIDEO_PATH: str 
    DEFAULT_VIDEO_PATH: str 


    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"


    # BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")
    # EMAIL_PORT: int = int(os.getenv("EMAIL_PORT", 587))
    # EMAIL_HOST_USER: str = os.getenv("EMAIL_HOST_USER")
    # EMAIL_HOST_PASSWORD: str = os.getenv("EMAIL_HOST_PASSWORD")
    # EMAIL_USE_TLS: bool = os.getenv("EMAIL_USE_TLS", "True").lower()
    # EMAIL_USE_SSL: bool = os.getenv("EMAIL_USE_SSL", "False").lower() == "true"
    # EMAIL_HOST: str = os.getenv("EMAIL_HOST", "smtp.example.com")

settings = Settings()
from log.log import setup_logger

logger = setup_logger()
logger.info("Settings loaded: %s", settings)