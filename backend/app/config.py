import os
import sys
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "New Codebase"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = ""

    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "new_codebase"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""
    DATABASE_URL: str = ""

    JWT_SECRET_KEY: str = ""
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_ALGORITHM: str = "HS256"

    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


def _build_settings() -> Settings:
    """Build and validate settings, returning a properly configured instance."""
    base_settings = Settings()

    errors = []
    overrides = {}

    if not base_settings.SECRET_KEY or base_settings.SECRET_KEY == "change-me-to-a-random-secret-key":
        errors.append("SECRET_KEY must be set to a secure random value via environment variable.")
        if not base_settings.SECRET_KEY:
            overrides["SECRET_KEY"] = "dev-only-secret-key-not-for-production"

    if not base_settings.JWT_SECRET_KEY or base_settings.JWT_SECRET_KEY == "change-me-to-a-random-jwt-secret":
        errors.append("JWT_SECRET_KEY must be set to a secure random value via environment variable.")
        if not base_settings.JWT_SECRET_KEY:
            overrides["JWT_SECRET_KEY"] = "dev-only-jwt-secret-not-for-production"

    if not base_settings.DATABASE_URL:
        errors.append("DATABASE_URL must be set via environment variable.")
        db_password = base_settings.DB_PASSWORD or "postgres"
        overrides["DATABASE_URL"] = f"postgresql+asyncpg://{base_settings.DB_USER}:{db_password}@{base_settings.DB_HOST}:{base_settings.DB_PORT}/{base_settings.DB_NAME}"

    if not base_settings.DB_PASSWORD or base_settings.DB_PASSWORD == "postgres":
        if base_settings.APP_ENV == "production":
            errors.append("DB_PASSWORD must be changed from default in production.")
        if not base_settings.DB_PASSWORD:
            overrides["DB_PASSWORD"] = "postgres"

    if errors and base_settings.APP_ENV == "production":
        for err in errors:
            print(f"CONFIGURATION ERROR: {err}", file=sys.stderr)
        sys.exit(1)
    elif errors and base_settings.APP_ENV != "production":
        for err in errors:
            print(f"WARNING: {err}", file=sys.stderr)

    # If we have overrides, create a new settings instance with them applied
    if overrides:
        # Get all current values and apply overrides
        env_values = {}
        for field_name in Settings.model_fields:
            env_values[field_name] = getattr(base_settings, field_name)
        env_values.update(overrides)
        return Settings(**env_values)

    return base_settings


settings = _build_settings()