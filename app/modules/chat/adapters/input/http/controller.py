from __future__ import annotations

import json
from collections.abc import Iterator

from app.modules.chat.adapters.input.http.schemas import (
    ConversationResponse,
    ConversationSummaryResponse,
    CreateConversationRequest,
    SendMessageRequest,
    SendMessageResponse,
)
from app.modules.chat.adapters.input.http.view_mapper import ChatViewMapper
from app.modules.chat.application.commands.create_conversation.create_conversation_command import (
    CreateConversationCommand,
)
from app.modules.chat.application.commands.send_message.send_message_command import (
    SendMessageCommand,
)
from app.modules.chat.application.ports.input.create_conversation_use_case import (
    CreateConversationUseCase,
)
from app.modules.chat.application.ports.input.get_conversation_use_case import (
    GetConversationUseCase,
)
from app.modules.chat.application.ports.input.list_conversations_use_case import (
    ListConversationsUseCase,
)
from app.modules.chat.application.ports.input.send_message_use_case import (
    SendMessageUseCase,
)
from app.modules.chat.application.queries.get_conversation.get_conversation_query import (
    GetConversationQuery,
)
from app.modules.chat.application.queries.list_conversations.list_conversations_query import (
    ListConversationsQuery,
)


class ChatController:
    """Thin inbound adapter: translate HTTP <-> use-case calls and map results
    to response schemas. No orchestration — that lives behind the use-case
    ports. Each method receives the use case it needs (injected by `routes.py`).
    """

    @staticmethod
    def create_conversation(
        request: CreateConversationRequest,
        use_case: CreateConversationUseCase,
    ) -> ConversationResponse:
        conversation = use_case.execute(
            CreateConversationCommand(title=request.title)
        )
        return ChatViewMapper.detail(conversation)

    @staticmethod
    def list_conversations(
        use_case: ListConversationsUseCase,
    ) -> list[ConversationSummaryResponse]:
        conversations = use_case.execute(ListConversationsQuery())
        return [ChatViewMapper.summary(c) for c in conversations]

    @staticmethod
    def get_conversation(
        conversation_id: str,
        use_case: GetConversationUseCase,
    ) -> ConversationResponse:
        conversation = use_case.execute(
            GetConversationQuery(conversation_id=conversation_id)
        )
        return ChatViewMapper.detail(conversation)

    @staticmethod
    def send_message(
        conversation_id: str,
        request: SendMessageRequest,
        use_case: SendMessageUseCase,
    ) -> SendMessageResponse:
        result = use_case.execute(
            SendMessageCommand(
                conversation_id=conversation_id, content=request.content
            )
        )
        return ChatViewMapper.send_result(result)

    @staticmethod
    def stream_message(
        conversation_id: str,
        request: SendMessageRequest,
        use_case: SendMessageUseCase,
    ) -> Iterator[str]:
        """Yield Server-Sent Events: one `token` event per chunk, then `done`."""
        command = SendMessageCommand(
            conversation_id=conversation_id, content=request.content
        )
        for chunk in use_case.execute_stream(command):
            yield _sse("token", {"content": chunk})
        yield _sse("done", {"conversation_id": conversation_id})


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"
