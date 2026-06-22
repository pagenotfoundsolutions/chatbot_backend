from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.chat.application.queries.list_messages.list_messages_query import (
    ListMessagesQuery,
)
from app.modules.chat.application.dto.message_dto import MessageDTO


class ListMessagesUseCase(ABC):
    """Inbound port: get paginated messages for a conversation."""

    @abstractmethod
    def execute(self, query: ListMessagesQuery) -> tuple[list[MessageDTO], int]:
        """Process the query."""
