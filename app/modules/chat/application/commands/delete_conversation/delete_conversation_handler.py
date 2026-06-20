from __future__ import annotations

from app.modules.chat.application.commands.delete_conversation.delete_conversation_command import (
    DeleteConversationCommand,
)
from app.modules.chat.application.ports.input.delete_conversation_use_case import (
    DeleteConversationUseCase,
)
from app.modules.chat.application.ports.output.conversation_repository_port import (
    ConversationRepositoryPort,
)
from app.modules.chat.domain.exceptions.chat_exceptions import ConversationNotFound


class DeleteConversationHandler(DeleteConversationUseCase):
    """Handles `DeleteConversationCommand`: load aggregate, verify owner, and delete."""

    def __init__(self, repository: ConversationRepositoryPort) -> None:
        self._repository = repository

    def execute(self, command: DeleteConversationCommand) -> None:
        conversation = self._repository.get(command.conversation_id)
        if conversation is None or conversation.auth_user_id != command.auth_user_id:
            raise ConversationNotFound(command.conversation_id)
        
        self._repository.delete(command.conversation_id)
