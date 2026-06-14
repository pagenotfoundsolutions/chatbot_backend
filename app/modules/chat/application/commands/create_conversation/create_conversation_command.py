from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateConversationCommand:
    """Intent to open a new conversation."""

    title: str | None = None
