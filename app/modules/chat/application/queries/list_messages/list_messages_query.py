from __future__ import annotations
import uuid

from dataclasses import dataclass


@dataclass(frozen=True)
class ListMessagesQuery:
    """Intent to fetch paginated messages for a specific conversation."""

    conversation_id: uuid.UUID
    auth_user_id: uuid.UUID
    page: int = 1
    size: int = 20
