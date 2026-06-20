from __future__ import annotations

from abc import abstractmethod

from app.modules.chat.domain.entities.conversation import Conversation
from app.modules.chat.domain.entities.message import Message
from app.shared.kernel.base_repository import BaseRepository


class ConversationRepositoryPort(BaseRepository[Conversation, str]):
    """Outbound (driven) port for persisting the Conversation aggregate.

    Extends the generic repository with chat-specific reads. The application
    depends on this interface only; a concrete adapter (SQLAlchemy, in-memory…)
    lives in `adapters/output/persistence`.
    """

    @abstractmethod
    def list(self, auth_user_id: str, page: int, size: int) -> tuple[list[Conversation], int]:
        """All conversations, most-recently-active first."""

    @abstractmethod
    def list_messages(self, conversation_id: str, auth_user_id: str, page: int, size: int) -> tuple[list[Message], int] | None:
        """Paginated list of messages for a specific conversation. Returns None if conversation not found/owned."""
