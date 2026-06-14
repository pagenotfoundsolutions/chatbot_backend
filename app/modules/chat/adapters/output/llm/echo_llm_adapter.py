from __future__ import annotations

from collections.abc import Iterator, Sequence

from app.modules.chat.application.ports.output.llm_port import LLMPort
from app.modules.chat.domain.entities.message import Message
from app.modules.chat.domain.value_objects.message_role import MessageRole


class EchoLLMAdapter(LLMPort):
    """A no-dependency stub implementation of the LLM port.

    It lets the whole chat flow run end-to-end with no API key, no model
    download, and no LangChain provider installed. It's the default provider
    (`LLM_PROVIDER=echo`); switch to a real one by setting `LLM_PROVIDER`.
    """

    def generate(self, history: Sequence[Message]) -> str:
        last_user = next(
            (m for m in reversed(history) if m.role == MessageRole.USER),
            None,
        )
        if last_user is None:
            return "Hello! How can I help you today?"
        return f"You said: {last_user.content}"

    def stream(self, history: Sequence[Message]) -> Iterator[str]:
        for token in self.generate(history).split(" "):
            yield token + " "
