from __future__ import annotations

from app.modules.chat.application.commands.create_conversation.create_conversation_command import (
    CreateConversationCommand,
)
from app.modules.chat.application.ports.input.create_conversation_use_case import (
    CreateConversationUseCase,
)
from app.modules.chat.application.ports.output.conversation_repository_port import (
    ConversationRepositoryPort,
)
from app.modules.chat.domain.entities.conversation import Conversation


class CreateConversationHandler(CreateConversationUseCase):
    """Handles `CreateConversationCommand`: start a fresh aggregate and persist."""

    def __init__(self, repository: ConversationRepositoryPort) -> None:
        self._repository = repository

    def execute(self, command: CreateConversationCommand) -> Conversation:
        conversation = Conversation.start(auth_user_id=command.auth_user_id, title=command.title)
        self._repository.save(conversation)
        return conversation
