from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ListConversationsQuery:
    """Intent to list conversation summaries, most-recently-active first."""
