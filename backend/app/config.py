import os
import warnings
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "New Codebase"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production"

    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "new_codebase"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/new_codebase"

    JWT_SECRET_KEY: str = "dev-jwt-secret-key-change-in-production"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_ALGORITHM: str = "HS256"

    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    @field_validator("SECRET_KEY")
    @classmethod
    def secret_key_must_be_set(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError(
                "SECRET_KEY must be set to a secure random value."
            )
        if v.startswith("<") and v.endswith(">"):
            warnings.warn(
                "SECRET_KEY appears to be a placeholder. "
                "Please set it to a secure random value for production.",
                stacklevel=2,
            )
        return v

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def jwt_secret_key_must_be_set(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError(
                "JWT_SECRET_KEY must be set to a secure random value."
            )
        if v.startswith("<") and v.endswith(">"):
            warnings.warn(
                "JWT_SECRET_KEY appears to be a placeholder. "
                "Please set it to a secure random value for production.",
                stacklevel=2,
            )
        return v

    @field_validator("DB_PASSWORD")
    @classmethod
    def db_password_must_be_set(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("DB_PASSWORD must be set via environment variable.")
        if v.startswith("<") and v.endswith(">"):
            warnings.warn(
                "DB_PASSWORD appears to be a placeholder. "
                "Please set it to a real password for production.",
                stacklevel=2,
            )
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def database_url_must_be_set(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("DATABASE_URL must be set via environment variable.")
        if "<" in v and ">" in v:
            warnings.warn(
                "DATABASE_URL appears to contain placeholder values. "
                "Please set it to a real connection string for production.",
                stacklevel=2,
            )
        return v

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()