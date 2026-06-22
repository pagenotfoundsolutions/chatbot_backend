from __future__ import annotations

import uuid
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
    def generate(self, history: Sequence[Message], config: ProviderConfigDTO) -> str:
        """Generate a single complete response from the LLM based on the conversation history."""
        pass

    @abstractmethod
    def stream(self, history: Sequence[Message], config: ProviderConfigDTO) -> Iterator[str]:
        """Yield the assistant reply as incremental text chunks.

        Default implementation falls back to a single chunk from `generate()`,
        so an adapter only overrides this when it supports true token streaming.
        """
        yield self.generate(history, config)
