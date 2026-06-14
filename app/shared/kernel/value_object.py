from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:
    """Base class for value objects.

    A value object has no identity — it is defined entirely by its attributes
    and is immutable. Subclass as a frozen dataclass and put validation in
    `__post_init__`. Equality and hashing come for free from the dataclass.

        @dataclass(frozen=True)
        class Email(ValueObject):
            value: str
            def __post_init__(self) -> None:
                if "@" not in self.value:
                    raise ValueError("invalid email")
    """
