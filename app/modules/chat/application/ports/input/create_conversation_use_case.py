from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.chat.application.commands.create_conversation.create_conversation_command import (
    CreateConversationCommand,
)
from app.modules.chat.domain.entities.conversation import Conversation


class CreateConversationUseCase(ABC):
    """Driving port: open a new conversation. Implemented by its command handler;
    inbound adapters depend only on this abstraction."""

    @abstractmethod
    def execute(self, command: CreateConversationCommand) -> Conversation:
        ...
