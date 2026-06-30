from __future__ import annotations
import uuid

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
    provider_id: uuid.UUID 
    model_id: uuid.UUID 
    thinking_enabled: bool = Field(default=False, description="Enable reasoning/thinking tokens for models that support it")
    file_id: uuid.UUID | None = Field(default=None, description="Optional ID of the document to use for RAG search")


# --- responses --------------------------------------------------------------
class MessageResponse(BaseModel):
    id: uuid.UUID
    role: MessageRole
    content: str
    thinking_content: str | None = None
    created_at: datetime


class ConversationSummaryResponse(BaseModel):
    """Conversation without its messages — for list views."""

    id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime


class ConversationResponse(ConversationSummaryResponse):
    """Full conversation including its message history."""

    messages: list[MessageResponse]


class SendMessageResponse(BaseModel):
    conversation_id: uuid.UUID
    user_message: MessageResponse
    assistant_message: MessageResponse
