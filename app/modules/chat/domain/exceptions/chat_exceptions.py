from __future__ import annotations

from app.shared.exceptions.exceptions import NotFoundException, ValidationException


class ConversationNotFound(NotFoundException):
    def __init__(self, conversation_id: str) -> None:
        super().__init__(f"Conversation '{conversation_id}' not found")


class EmptyMessageContent(ValidationException):
    def __init__(self) -> None:
        super().__init__("Message content cannot be empty")
