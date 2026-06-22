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
from app.modules.chat.application.dto.conversation_dto import ConversationDTO


class ListConversationsHandler(ListConversationsUseCase):
    """Handles `ListConversationsQuery`: return conversation summaries."""

    def __init__(self, repository: ConversationRepositoryPort) -> None:
        self._repository = repository

    def execute(self, query: ListConversationsQuery) -> tuple[list[ConversationDTO], int]:
        conversations, total = self._repository.list(
            auth_user_id=query.auth_user_id,
            page=query.page,
            size=query.size,
        )
        return [ConversationDTO.from_entity(c) for c in conversations], total
