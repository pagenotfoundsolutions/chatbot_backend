from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


def _new_id() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class DomainEvent:
    """Base class for domain events — an immutable record that something
    business-meaningful happened.

    Concrete events subclass this and add their own payload fields. The
    `event_id` / `occurred_at` metadata is filled in automatically. Events are
    raised by aggregates and (later) dispatched by the application layer to an
    `EventPublisherPort`.
    """

    event_id: str = field(default_factory=_new_id, init=False)
    occurred_at: datetime = field(default_factory=_now, init=False)
