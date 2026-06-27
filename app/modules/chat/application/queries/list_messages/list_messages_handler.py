from __future__ import annotations

from app.modules.chat.application.dto.message_dto import MessageDTO
from app.modules.chat.application.ports.input.list_messages_use_case import (
    ListMessagesUseCase,
)
from app.modules.chat.application.ports.output.conversation_repository_port import (
    ConversationRepositoryPort,
)
from app.modules.chat.application.queries.list_messages.list_messages_query import (
    ListMessagesQuery,
)
from app.modules.chat.domain.exceptions.chat_exceptions import ConversationNotFound


class ListMessagesHandler(ListMessagesUseCase):
    """Handles `ListMessagesQuery`: return paginated messages."""

    def __init__(self, repository: ConversationRepositoryPort) -> None:
        self._repository = repository

    def execute(self, query: ListMessagesQuery) -> tuple[list[MessageDTO], int]:
        result = self._repository.list_messages(
            query.conversation_id, query.auth_user_id, query.page, query.size
        )
        if result is None:
            raise ConversationNotFound(query.conversation_id)
        messages, total = result
        return [MessageDTO.from_entity(m) for m in messages], total
