from __future__ import annotations

from typing import TYPE_CHECKING

from app.modules.chat.infrastructure.config.chat_config import ChatConfig

if TYPE_CHECKING:
    from langchain_core.language_models.chat_models import BaseChatModel


def build_chat_model(config: ChatConfig) -> "BaseChatModel":
    """Construct a LangChain chat model for the configured provider.

    Each provider's integration package is imported lazily so that only the one
    actually selected needs to be installed. A missing package raises a clear,
    actionable error rather than failing at import time for everyone.
    """
    provider = config.provider.lower()
    model = config.resolved_model()

    if provider in ("anthropic", "openai"):
        # `init_chat_model` is LangChain's provider-agnostic entry point; it
        # picks the right integration (langchain-anthropic / langchain-openai).
        from langchain.chat_models import init_chat_model

        return init_chat_model(
            model,
            model_provider=provider,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )

    if provider == "ollama":
        try:
            from langchain_ollama import ChatOllama
        except ImportError as exc:  # pragma: no cover - dependency guard
            raise RuntimeError(
                "LLM_PROVIDER=ollama requires the 'langchain-ollama' package."
            ) from exc
        return ChatOllama(
            model=model,
            base_url=config.ollama_base_url,
            temperature=config.temperature,
        )

    if provider == "huggingface":
        try:
            from langchain_huggingface import (
                ChatHuggingFace,
                HuggingFaceEndpoint,
            )
        except ImportError as exc:  # pragma: no cover - dependency guard
            raise RuntimeError(
                "LLM_PROVIDER=huggingface requires the 'langchain-huggingface' package."
            ) from exc
        endpoint = HuggingFaceEndpoint(
            repo_id=model,
            task="text-generation",
            temperature=config.temperature,
            max_new_tokens=config.max_tokens,
        )
        return ChatHuggingFace(llm=endpoint)

    raise ValueError(
        f"Unsupported LLM_PROVIDER '{config.provider}'. "
        "Use one of: anthropic, openai, ollama, huggingface, echo."
    )
