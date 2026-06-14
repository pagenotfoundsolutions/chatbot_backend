from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# .env lives at the project root: .../pdf-rag/.env
_ENV_FILE = Path(__file__).resolve().parents[5] / ".env"


class AuthConfig(BaseSettings):
    """Configuration for the Auth module."""

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        env_prefix="AUTH_",
        extra="ignore",
    )

    jwt_secret_key: str = "a_very_secret_default_key_for_development_only"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7


@lru_cache
def get_auth_config() -> AuthConfig:
    """Build AuthConfig once and cache it (singleton)."""
    return AuthConfig()
