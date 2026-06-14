from __future__ import annotations

from typing import Generic, TypeVar

from app.shared.kernel.domain_event import DomainEvent
from app.shared.kernel.entity import Entity

TId = TypeVar("TId")


class AggregateRoot(Entity[TId], Generic[TId]):
    """Base class for aggregate roots — the consistency boundary of the domain.

    Outside code mutates an aggregate only through its root's methods, so the
    root can keep its invariants intact. The root also records `DomainEvent`s as
    state changes happen; the application layer pulls them with `pull_events()`
    after a successful save and hands them to a publisher.
    """

    def __init__(self, id: TId) -> None:
        super().__init__(id)
        self._events: list[DomainEvent] = []

    def record(self, event: DomainEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[DomainEvent]:
        """Return and clear the buffered events (drain semantics)."""
        events, self._events = self._events, []
        return events
