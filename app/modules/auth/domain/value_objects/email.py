from dataclasses import dataclass
import re
from app.shared.kernel.value_object import ValueObject

@dataclass(frozen=True)
class Email(ValueObject):
    value: str

    def __post_init__(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise ValueError(f"Invalid email format: {self.value}")

