from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.chat.application.commands.delete_conversation.delete_conversation_command import (
    DeleteConversationCommand,
)


class DeleteConversationUseCase(ABC):
    """Inbound port: delete a conversation."""

    @abstractmethod
    def execute(self, command: DeleteConversationCommand) -> None:
        """Process the delete command."""
