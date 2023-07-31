from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Config(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ALGORITHM: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_OAUTH2_TOKEN_URL: str
    GOOGLE_OAUTH2_USERINFO_URL: str
    GOOGLE_OAUTH2_REDIRECT_LOGIN: str
    GOOGLE_OAUTH2_REDIRECT_REGISTER: str

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    CORS_ALLOW_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    APP_VERSION: str = "1"
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


@lru_cache()
def get_settings():
    return Config()