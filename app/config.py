from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path
import os


ENV_PATH = Path(__file__).resolve().parent

class Config(BaseSettings):
    bluesky_username: str
    bluesky_password: str
    bluesky_did: str    
    bluesky_session_url: str
    bluesky_post_url: str
    mastodon_username: str
    mastodon_access_token: str      
    mastodon_post_url: str
    devto_username: str
    devto_api_key: str
    devto_post_url: str
    gist_pat_token: str
    gist_post_url: str
    telegram_api_token: str
    telegram_base_url: str
    telegram_channel_url: str
    telegram_channel_id: str
    
    model_config = SettingsConfigDict(env_file=ENV_PATH / ".env",
        env_file_encoding="utf-8",
        extra="ignore")
    

@lru_cache(maxsize=1)
def get_cached_config(mtime : float) -> Config:
    return Config()

def get_config() -> Config:
    mtime = os.path.getmtime(ENV_PATH) if ENV_PATH.exists() else 0.0
    return get_cached_config(mtime)