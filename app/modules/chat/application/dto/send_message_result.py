from __future__ import annotations

from dataclasses import dataclass

from app.modules.chat.application.dto.conversation_dto import ConversationDTO
from app.modules.chat.application.dto.message_dto import MessageDTO


@dataclass(frozen=True)
class SendMessageResult:
    """Outcome of one chat turn: the persisted user message and the assistant's
    reply, plus the conversation they belong to."""

    conversation: ConversationDTO
    user_message: MessageDTO
    assistant_message: MessageDTO
