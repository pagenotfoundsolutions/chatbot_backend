from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.chat.application.commands.update_conversation.update_conversation_command import (
    UpdateConversationCommand,
)


class UpdateConversationUseCase(ABC):
    """Inbound port: update a conversation."""

    @abstractmethod
    def execute(self, command: UpdateConversationCommand) -> None:
        """Process the update command."""
