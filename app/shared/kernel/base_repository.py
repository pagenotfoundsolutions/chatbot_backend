from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TAggregate = TypeVar("TAggregate")
TId = TypeVar("TId")


class BaseRepository(ABC, Generic[TAggregate, TId]):
    """Generic outbound port for aggregate persistence.

    This is a domain-facing *interface* only — concrete implementations live in
    a module's `adapters/output/persistence`. Module-specific repository ports
    extend this with their own query methods.
    """

    @abstractmethod
    def save(self, aggregate: TAggregate) -> None:
        """Insert or update the aggregate as a whole."""

    @abstractmethod
    def get(self, id: TId) -> TAggregate | None:
        """Load the full aggregate by id, or None if absent."""

    @abstractmethod
    def delete(self, id: TId) -> None:
        """Remove the aggregate by id (no-op if absent)."""
