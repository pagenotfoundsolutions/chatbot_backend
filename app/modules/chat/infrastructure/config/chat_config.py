from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# .env lives at the project root: .../pdf-rag/.env
_ENV_FILE = Path(__file__).resolve().parents[5] / ".env"

# Sensible per-provider default model when LLM_MODEL is not set.
_DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-4-6",
    "openai": "gpt-4o-mini",
    "ollama": "llama3.1",
    "huggingface": "HuggingFaceH4/zephyr-7b-beta",
    "echo": "echo",
}


class ChatConfig(BaseSettings):
    """LLM configuration for the chat module.

    Driven entirely by env vars (prefix `LLM_`). The `provider` selects which
    backend the LangChain/LangGraph adapter builds; everything else is optional
    with safe defaults so the app boots without any keys (provider=`echo`).
    """

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        env_prefix="LLM_",
        extra="ignore",
    )

    # anthropic | openai | ollama | huggingface | echo
    provider: str = "echo"
    model: str | None = None
    temperature: float = 0.7
    max_tokens: int = 1024
    system_prompt: str = "You are a helpful assistant."

    # Ollama base url (only used when provider=ollama).
    ollama_base_url: str = "http://localhost:11434"

    def resolved_model(self) -> str:
        """The model id to use — explicit `LLM_MODEL` or the provider default."""
        if self.model:
            return self.model
        return _DEFAULT_MODELS.get(self.provider, _DEFAULT_MODELS["echo"])


@lru_cache
def get_chat_config() -> ChatConfig:
    """Build ChatConfig once and cache it (singleton)."""
    return ChatConfig()
