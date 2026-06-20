from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteConversationCommand:
    """Intent to delete a conversation."""

    conversation_id: str
    auth_user_id: str
