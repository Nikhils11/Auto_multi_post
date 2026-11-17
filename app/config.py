from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent

class Config(BaseSettings):
    bluesky_username: str
    bluesky_password: str
    bluesky_did: str
    model_config = SettingsConfigDict(env_file=APP_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore")
    

@lru_cache()
def get_config() -> Config:
    return Config()
    