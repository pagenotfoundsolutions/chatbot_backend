from functools import lru_cache
from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


from urllib.parse import quote_plus

# Runtime differences live in one local env file; Compose injects the same file.
_ENV_FILE = Path(__file__).resolve().parents[3] / "env" / ".env"


class Settings(BaseSettings):
    # read values from .env. fields have NO defaults -> they are REQUIRED:
    # if a var is missing in .env, the app fails fast at startup.
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- project metadata ---
    project_name: str
    description: str
    version: str
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "https://chatbot.pagenotfoundsolutions.cloud",
    ]
    
    # --- LLM API Keys ---
    nvidia_api_key: str | None = None

    # --- database ---
    database_url: str

    postgres_user: str
    postgres_password: str
    postgres_db: str

    @model_validator(mode="after")
    def interpolate_db_url(self) -> "Settings":
        if self.database_url:
            self.database_url = self.database_url.replace("${POSTGRES_USER}", self.postgres_user)
            # Credentials may contain URL-reserved characters such as ``@``.
            # Encode them before inserting them into the SQLAlchemy URL.
            self.database_url = self.database_url.replace(
                "${POSTGRES_PASSWORD}", quote_plus(self.postgres_password)
            )
            self.database_url = self.database_url.replace("${POSTGRES_DB}", self.postgres_db)
        return self

    # --- storage paths ---
    upload_dir: str

    # --- SMTP ---
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    smtp_use_tls: bool = True


@lru_cache
def get_settings() -> Settings:
    """Build Settings once and cache it (singleton)."""
    return Settings()


# import this everywhere: `from app.shared.config.settings import settings`
settings = get_settings()
