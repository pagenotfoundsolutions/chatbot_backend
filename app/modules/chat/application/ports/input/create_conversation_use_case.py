from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.chat.application.commands.create_conversation.create_conversation_command import (
    CreateConversationCommand,
)
from app.modules.chat.application.dto.conversation_dto import ConversationDTO


class CreateConversationUseCase(ABC):
    """Driving port: create a new conversation."""

    @abstractmethod
    def execute(self, command: CreateConversationCommand) -> ConversationDTO:
        ...
