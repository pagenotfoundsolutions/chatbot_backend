from __future__ import annotations

from dataclasses import dataclass

from app.modules.chat.domain.value_objects.message_role import MessageRole
from app.shared.kernel.domain_event import DomainEvent


@dataclass(frozen=True)
class MessagePosted(DomainEvent):
    """Raised by the Conversation aggregate whenever a message is appended."""

    conversation_id: str = ""
    message_id: str = ""
    role: MessageRole = MessageRole.USER
