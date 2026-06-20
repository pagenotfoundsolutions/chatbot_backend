from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.modules.chat.domain.exceptions.chat_exceptions import EmptyMessageContent
from app.modules.chat.domain.value_objects.message_role import MessageRole
from app.shared.kernel.entity import Entity


from app.shared.kernel.utils import generate_uuid, utc_now


class Message(Entity[str]):
    """A single turn in a conversation. Entity inside the Conversation aggregate.

    Identity is `id` (handled by the Entity base): two messages are the same iff
    they share an id.
    """

    def __init__(
        self,
        id: str,
        role: MessageRole,
        content: str,
        created_at: datetime,
    ) -> None:
        if not content or not content.strip():
            raise EmptyMessageContent()
        super().__init__(id)
        self._role = role
        self._content = content
        self._created_at = created_at

    @classmethod
    def create(cls, role: MessageRole, content: str) -> "Message":
        return cls(id=generate_uuid(), role=role, content=content, created_at=utc_now())

    @property
    def role(self) -> MessageRole:
        return self._role

    @property
    def content(self) -> str:
        return self._content

    @property
    def created_at(self) -> datetime:
        return self._created_at
