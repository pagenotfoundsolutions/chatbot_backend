from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateConversationCommand:
    """Intent to update a conversation's title."""

    conversation_id: str
    auth_user_id: str
    title: str
