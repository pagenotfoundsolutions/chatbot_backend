from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.chat.application.queries.list_messages.list_messages_query import (
    ListMessagesQuery,
)
from app.modules.chat.domain.entities.message import Message


class ListMessagesUseCase(ABC):
    """Inbound port: get paginated messages for a conversation."""

    @abstractmethod
    def execute(self, query: ListMessagesQuery) -> tuple[list[Message], int]:
        """Process the query."""
