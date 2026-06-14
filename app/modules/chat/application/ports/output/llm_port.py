from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator, Sequence

from app.modules.chat.domain.entities.message import Message


class LLMPort(ABC):
    """Outbound (driven) port for the text-generation backend.

    The application hands over the conversation so far and gets back the
    assistant's reply. Swapping echo-stub -> a real provider (OpenAI, Anthropic,
    Ollama, a local HF model) is purely an adapter change behind this seam; the
    core never moves.
    """

    @abstractmethod
    def generate(self, history: Sequence[Message]) -> str:
        """Produce the full assistant reply for the given message history.

        `history` is chronological and includes the latest user message.
        """

    def stream(self, history: Sequence[Message]) -> Iterator[str]:
        """Yield the assistant reply as incremental text chunks.

        Default implementation falls back to a single chunk from `generate()`,
        so an adapter only overrides this when it supports true token streaming.
        """
        yield self.generate(history)
