from __future__ import annotations

from abc import abstractmethod

from app.modules.chat.domain.entities.conversation import Conversation
from app.shared.kernel.base_repository import BaseRepository


class ConversationRepositoryPort(BaseRepository[Conversation, str]):
    """Outbound (driven) port for persisting the Conversation aggregate.

    Extends the generic repository with chat-specific reads. The application
    depends on this interface only; a concrete adapter (SQLAlchemy, in-memory…)
    lives in `adapters/output/persistence`.
    """

    @abstractmethod
    def list(self) -> list[Conversation]:
        """All conversations, most-recently-active first."""
