from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.chat.application.queries.list_conversations.list_conversations_query import (
    ListConversationsQuery,
)
from app.modules.chat.application.dto.conversation_dto import ConversationDTO


class ListConversationsUseCase(ABC):
    """Driving port: paginate through a user's conversations."""

    @abstractmethod
    def execute(self, query: ListConversationsQuery) -> tuple[list[ConversationDTO], int]:
        ...
