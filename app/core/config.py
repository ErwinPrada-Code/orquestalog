from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sistema de Orquestación Logística Multiempresa"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/orquestalog"
    SECRET_KEY: str = "super_secret_key_jwt_orquestalog_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 día

    class Config:
        env_file = ".env"

settings = Settings()