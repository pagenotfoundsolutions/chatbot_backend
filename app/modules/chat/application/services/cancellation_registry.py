from uuid import UUID

class StreamCancellationRegistry:
    """Simple in-memory registry to track and signal stream cancellation requests."""
    
    _registry: set[UUID] = set()

    @classmethod
    def request_cancellation(cls, conversation_id: UUID) -> None:
        cls._registry.add(conversation_id)

    @classmethod
    def is_cancelled(cls, conversation_id: UUID) -> bool:
        return conversation_id in cls._registry

    @classmethod
    def clear(cls, conversation_id: UUID) -> None:
        cls._registry.discard(conversation_id)
