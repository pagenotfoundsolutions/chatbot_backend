from __future__ import annotations

from app.modules.chat.adapters.input.http.schemas import (
    ConversationResponse,
    ConversationSummaryResponse,
    MessageResponse,
    SendMessageResponse,
)
from app.modules.chat.application.dto.send_message_result import SendMessageResult
from app.modules.chat.domain.entities.conversation import Conversation
from app.modules.chat.domain.entities.message import Message


class ChatViewMapper:
    """Domain aggregate -> API response schemas (the inbound adapter's seam)."""

    @staticmethod
    def message(message: Message) -> MessageResponse:
        return MessageResponse(
            id=message.id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
        )

    @staticmethod
    def summary(conversation: Conversation) -> ConversationSummaryResponse:
        return ConversationSummaryResponse(
            id=conversation.id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
        )

    @staticmethod
    def detail(conversation: Conversation) -> ConversationResponse:
        return ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=[ChatViewMapper.message(m) for m in conversation.messages],
        )

    @staticmethod
    def send_result(result: SendMessageResult) -> SendMessageResponse:
        return SendMessageResponse(
            conversation_id=result.conversation.id,
            user_message=ChatViewMapper.message(result.user_message),
            assistant_message=ChatViewMapper.message(result.assistant_message),
        )
