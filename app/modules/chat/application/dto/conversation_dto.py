from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from app.modules.chat.application.dto.message_dto import MessageDTO
from app.modules.chat.domain.entities.conversation import Conversation

@dataclass(frozen=True)
class ConversationDTO:
    """Application DTO representing a full conversation."""
    id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[MessageDTO]

    @classmethod
    def from_entity(cls, entity: Conversation) -> ConversationDTO:
        return cls(
            id=entity.id,
            title=entity.title,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            messages=[MessageDTO.from_entity(m) for m in entity.messages],
        )
