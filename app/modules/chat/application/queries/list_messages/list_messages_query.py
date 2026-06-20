from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ListMessagesQuery:
    """Intent to fetch paginated messages for a specific conversation."""

    conversation_id: str
    auth_user_id: str
    page: int = 1
    size: int = 20
