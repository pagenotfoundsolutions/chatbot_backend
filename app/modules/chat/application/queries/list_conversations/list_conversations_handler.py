from __future__ import annotations

from app.modules.chat.application.ports.input.list_conversations_use_case import (
    ListConversationsUseCase,
)
from app.modules.chat.application.ports.output.conversation_repository_port import (
    ConversationRepositoryPort,
)
from app.modules.chat.application.queries.list_conversations.list_conversations_query import (
    ListConversationsQuery,
)
from app.modules.chat.domain.entities.conversation import Conversation


class ListConversationsHandler(ListConversationsUseCase):
    """Handles `ListConversationsQuery`: return conversation summaries."""

    def __init__(self, repository: ConversationRepositoryPort) -> None:
        self._repository = repository

    def execute(self, query: ListConversationsQuery) -> tuple[list[Conversation], int]:
        return self._repository.list(query.auth_user_id, query.page, query.size)
