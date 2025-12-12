from pydantic_settings import BaseSettings
from log.log import setup_logger

class Settings(BaseSettings):
    PHOTO_PATH: str 
    DEFAULT_PHOTO_PATH: str 
    VIDEO_PATH: str 
    DEFAULT_VIDEO_PATH: str 
    ALTERNATIVE_EMAIL_HOST_USER : str
    ALTERNATIVE_EMAIL_HOST_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
logger = setup_logger()