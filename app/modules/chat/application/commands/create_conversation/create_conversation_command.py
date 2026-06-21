from __future__ import annotations
import uuid

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateConversationCommand:
    """Intent to open a new conversation."""

    auth_user_id: uuid.UUID
    title: str | None = None
