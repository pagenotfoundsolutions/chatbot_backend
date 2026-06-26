from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator

from app.modules.chat.application.commands.send_message.send_message_command import (
    SendMessageCommand,
)
from app.modules.chat.application.dto.send_message_result import SendMessageResult


class SendMessageUseCase(ABC):
    """Driving port: post a user message and produce the assistant's reply."""

    @abstractmethod
    def execute(self, command: SendMessageCommand) -> SendMessageResult:
        """Run one full turn and return the persisted result."""

    @abstractmethod
    def execute_stream(self, command: SendMessageCommand) -> Iterator[tuple[str, str]]:
        """Run one turn, streaming the assistant reply as text chunks (type, content).

        Persists the completed turn once the stream is exhausted.
        """
