from __future__ import annotations

from app.modules.chat.application.commands.update_conversation.update_conversation_command import (
    UpdateConversationCommand,
)
from app.modules.chat.application.ports.input.update_conversation_use_case import (
    UpdateConversationUseCase,
)
from app.modules.chat.application.ports.output.conversation_repository_port import (
    ConversationRepositoryPort,
)
from app.modules.chat.domain.exceptions.chat_exceptions import ConversationNotFound


class UpdateConversationHandler(UpdateConversationUseCase):
    """Handles `UpdateConversationCommand`: load aggregate, verify owner, update title and save."""

    def __init__(self, repository: ConversationRepositoryPort) -> None:
        self._repository = repository

    def execute(self, command: UpdateConversationCommand) -> None:
        conversation = self._repository.get(command.conversation_id)
        if conversation is None or conversation.auth_user_id != command.auth_user_id:
            raise ConversationNotFound(command.conversation_id)
        
        conversation.rename(command.title)
        self._repository.save(conversation)
