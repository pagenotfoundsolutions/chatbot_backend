from __future__ import annotations

from typing import Generic, TypeVar

TId = TypeVar("TId")


class Entity(Generic[TId]):
    """Base class for domain entities.

    An entity has a stable identity: two entities are equal iff they share the
    same id, regardless of their other attributes. This is what distinguishes an
    entity from a value object (which is equal by its whole value).
    """

    def __init__(self, id: TId) -> None:
        self._id = id

    @property
    def id(self) -> TId:
        return self._id

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and self._id == other._id  # type: ignore[attr-defined]

    def __hash__(self) -> int:
        return hash((type(self), self._id))
