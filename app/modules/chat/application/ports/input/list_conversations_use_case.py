from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.chat.application.queries.list_conversations.list_conversations_query import (
    ListConversationsQuery,
)
from app.modules.chat.domain.entities.conversation import Conversation


class ListConversationsUseCase(ABC):
    """Driving port: list conversations, most-recently-active first."""

    @abstractmethod
    def execute(self, query: ListConversationsQuery) -> list[Conversation]:
        ...
