from __future__ import annotations

from dataclasses import dataclass

from app.modules.chat.domain.entities.conversation import Conversation
from app.modules.chat.domain.entities.message import Message


@dataclass(frozen=True)
class SendMessageResult:
    """Outcome of one chat turn: the persisted user message and the assistant's
    reply, plus the conversation they belong to."""

    conversation: Conversation
    user_message: Message
    assistant_message: Message
