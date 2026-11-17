from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Config(BaseSettings):
    bluesky_username: str
    bluesky_password: str
    bluesky_did: str
    model_config = SettingsConfigDict(env_file= ".env", extra= "ignore")
    

@lru_cache()
def get_config() -> Config:
    return Config()
    