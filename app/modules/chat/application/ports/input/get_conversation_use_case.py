from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.chat.application.queries.get_conversation.get_conversation_query import (
    GetConversationQuery,
)
from app.modules.chat.domain.entities.conversation import Conversation


class GetConversationUseCase(ABC):
    """Driving port: read one conversation with its messages."""

    @abstractmethod
    def execute(self, query: GetConversationQuery) -> Conversation:
        ...
