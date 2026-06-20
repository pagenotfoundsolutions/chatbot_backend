from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SendMessageCommand:
    """Intent to post a user message to a conversation and get the reply."""

    conversation_id: str
    auth_user_id: str
    content: str
