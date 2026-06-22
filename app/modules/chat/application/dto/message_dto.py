from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from app.modules.chat.domain.value_objects.message_role import MessageRole
from app.modules.chat.domain.entities.message import Message

@dataclass(frozen=True)
class MessageDTO:
    """Application DTO representing a chat message."""
    id: uuid.UUID
    role: MessageRole
    content: str
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: Message) -> MessageDTO:
        return cls(
            id=entity.id,
            role=entity.role,
            content=entity.content,
            created_at=entity.created_at,
        )
