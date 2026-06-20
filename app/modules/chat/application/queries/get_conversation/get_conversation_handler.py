from __future__ import annotations

from app.modules.chat.application.ports.input.get_conversation_use_case import (
    GetConversationUseCase,
)
from app.modules.chat.application.ports.output.conversation_repository_port import (
    ConversationRepositoryPort,
)
from app.modules.chat.application.queries.get_conversation.get_conversation_query import (
    GetConversationQuery,
)
from app.modules.chat.domain.entities.conversation import Conversation
from app.modules.chat.domain.exceptions.chat_exceptions import ConversationNotFound


class GetConversationHandler(GetConversationUseCase):
    """Handles `GetConversationQuery`: load one aggregate or raise if absent."""

    def __init__(self, repository: ConversationRepositoryPort) -> None:
        self._repository = repository

    def execute(self, query: GetConversationQuery) -> Conversation:
        conversation = self._repository.get(query.conversation_id)
        if conversation is None or conversation.auth_user_id != query.auth_user_id:
            raise ConversationNotFound(query.conversation_id)
        return conversation
