from __future__ import annotations
import uuid

from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteConversationCommand:
    """Intent to delete a conversation."""

    conversation_id: uuid.UUID
    auth_user_id: uuid.UUID
