from __future__ import annotations
import uuid

from dataclasses import dataclass


@dataclass(frozen=True)
class SendMessageCommand:
    """Intent to post a user message to a conversation and get the reply."""

    conversation_id: uuid.UUID
    auth_user_id: uuid.UUID
    content: str
    provider_id: uuid.UUID
    model_id: uuid.UUID
    file_id: uuid.UUID | None = None

