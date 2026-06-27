from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator, Sequence

from app.modules.chat.domain.entities.message import Message
from app.modules.ai_providers.application.dto.provider_config_dto import ProviderConfigDTO


class LLMPort(ABC):
    """Outbound (driven) port for the text-generation backend.

    The application hands over the conversation so far and gets back the
    assistant's reply. Swapping echo-stub -> a real provider (OpenAI, Anthropic,
    Ollama, a local HF model) is purely an adapter change behind this seam; the
    core never moves.
    """

    @abstractmethod
    def generate(self, history: Sequence[Message], config: ProviderConfigDTO, thinking_enabled: bool = False, context: dict | None = None) -> str:
        """Generate a single complete response from the LLM based on the conversation history."""
        pass

    @abstractmethod
    def stream(self, history: Sequence[Message], config: ProviderConfigDTO, thinking_enabled: bool = False, context: dict | None = None) -> Iterator[tuple[str, str]]:
        """Yield the assistant reply as incremental text chunks (type, content).
        Type can be 'content' or 'thinking'.

        Default implementation falls back to a single chunk from `generate()`,
        so an adapter only overrides this when it supports true token streaming.
        """
        yield "content", self.generate(history, config, thinking_enabled, context)
