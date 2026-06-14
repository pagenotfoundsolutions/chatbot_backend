from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GetConversationQuery:
    """Intent to read a single conversation with its full message history."""

    conversation_id: str
