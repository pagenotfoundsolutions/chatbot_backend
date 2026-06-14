from enum import Enum


class MessageRole(str, Enum):
    """Who authored a message inside a conversation.

    Mirrors the ChatGPT-style roles. `str` mixin so it serialises cleanly to
    JSON / DB and compares equal to the raw string value.
    """

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
