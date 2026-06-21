from __future__ import annotations
import uuid

from dataclasses import dataclass


@dataclass(frozen=True)
class GetConversationQuery:
    """Intent to read a single conversation with its full message history."""

    conversation_id: uuid.UUID
    auth_user_id: uuid.UUID
