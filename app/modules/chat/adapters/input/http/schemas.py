from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.modules.chat.domain.value_objects.message_role import MessageRole


# --- requests ---------------------------------------------------------------
class CreateConversationRequest(BaseModel):
    title: str | None = Field(default=None, max_length=255)


class UpdateConversationRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class SendMessageRequest(BaseModel):
    content: str = Field(min_length=1)


# --- responses --------------------------------------------------------------
class MessageResponse(BaseModel):
    id: str
    role: MessageRole
    content: str
    created_at: datetime


class ConversationSummaryResponse(BaseModel):
    """Conversation without its messages — for list views."""

    id: str
    title: str
    created_at: datetime
    updated_at: datetime


class ConversationResponse(ConversationSummaryResponse):
    """Full conversation including its message history."""

    messages: list[MessageResponse]


class SendMessageResponse(BaseModel):
    conversation_id: str
    user_message: MessageResponse
    assistant_message: MessageResponse
