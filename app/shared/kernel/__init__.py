"""Shared kernel — DDD building blocks reused by every module's domain."""

from app.shared.kernel.aggregate_root import AggregateRoot
from app.shared.kernel.base_repository import BaseRepository
from app.shared.kernel.domain_event import DomainEvent
from app.shared.kernel.entity import Entity
from app.shared.kernel.value_object import ValueObject

__all__ = [
    "AggregateRoot",
    "BaseRepository",
    "DomainEvent",
    "Entity",
    "ValueObject",
]
