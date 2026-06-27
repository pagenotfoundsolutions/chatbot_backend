from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime


from app.shared.kernel.utils import generate_uuid, utc_now


@dataclass(frozen=True)
class DomainEvent:
    """Base class for domain events — an immutable record that something
    business-meaningful happened.

    Concrete events subclass this and add their own payload fields. The
    `event_id` / `occurred_at` metadata is filled in automatically. Events are
    raised by aggregates and (later) dispatched by the application layer to an
    `EventPublisherPort`.
    """

    event_id: uuid.UUID = field(default_factory=generate_uuid, init=False)
    occurred_at: datetime = field(default_factory=utc_now, init=False)
