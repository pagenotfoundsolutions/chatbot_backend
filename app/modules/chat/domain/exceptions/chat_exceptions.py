from __future__ import annotations
import uuid

from app.shared.exceptions.exceptions import NotFoundException, ValidationException, AppException


class ConversationNotFound(NotFoundException):
    def __init__(self, conversation_id: uuid.UUID) -> None:
        super().__init__(f"Conversation '{conversation_id}' not found")


class EmptyMessageContent(ValidationException):
    def __init__(self) -> None:
        super().__init__("Message content cannot be empty")


class ProviderConfigurationNotFound(NotFoundException):
    def __init__(self, provider_id: uuid.UUID, model_id: uuid.UUID) -> None:
        super().__init__(f"Provider configuration not found for Provider '{provider_id}' and Model '{model_id}'")


class RAGRetrievalFailed(AppException):
    def __init__(self, reason: str) -> None:
        super().__init__(f"Failed to retrieve documents for RAG context: {reason}", status_code=500)
