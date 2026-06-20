from __future__ import annotations

import json
from collections.abc import Iterator

from app.modules.chat.adapters.input.http.schemas import (
    ConversationResponse,
    ConversationSummaryResponse,
    MessageResponse,
    CreateConversationRequest,
    UpdateConversationRequest,
    SendMessageRequest,
    SendMessageResponse,
)
from app.modules.chat.adapters.input.http.view_mapper import ChatViewMapper
from app.shared.pagination import Page
from app.modules.chat.application.commands.create_conversation.create_conversation_command import (
    CreateConversationCommand,
)
from app.modules.chat.application.commands.send_message.send_message_command import (
    SendMessageCommand,
)
from app.modules.chat.application.ports.input.create_conversation_use_case import (
    CreateConversationUseCase,
)
from app.modules.chat.application.ports.input.delete_conversation_use_case import (
    DeleteConversationUseCase,
)
from app.modules.chat.application.ports.input.get_conversation_use_case import (
    GetConversationUseCase,
)
from app.modules.chat.application.ports.input.list_conversations_use_case import (
    ListConversationsUseCase,
)
from app.modules.chat.application.ports.input.list_messages_use_case import (
    ListMessagesUseCase,
)
from app.modules.chat.application.ports.input.update_conversation_use_case import (
    UpdateConversationUseCase,
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
from app.modules.chat.application.queries.list_messages.list_messages_query import (
    ListMessagesQuery,
)


from app.modules.chat.application.commands.delete_conversation.delete_conversation_command import (
    DeleteConversationCommand,
)
from app.modules.chat.application.commands.update_conversation.update_conversation_command import (
    UpdateConversationCommand,
)

class ChatController:
    """Thin inbound adapter: translate HTTP <-> use-case calls and map results
    to response schemas. No orchestration — that lives behind the use-case
    ports. Each method receives the use case it needs (injected by `routes.py`).
    """

    @staticmethod
    def create_conversation(
        auth_user_id: str,
        request: CreateConversationRequest,
        use_case: CreateConversationUseCase,
    ) -> ConversationResponse:
        conversation = use_case.execute(
            CreateConversationCommand(auth_user_id=auth_user_id, title=request.title)
        )
        return ChatViewMapper.detail(conversation)

    @staticmethod
    def list_conversations(
        auth_user_id: str,
        page: int,
        size: int,
        use_case: ListConversationsUseCase,
    ) -> Page[ConversationSummaryResponse]:
        conversations, total = use_case.execute(
            ListConversationsQuery(auth_user_id=auth_user_id, page=page, size=size)
        )
        return Page.create(
            items=[ChatViewMapper.summary(c) for c in conversations],
            total=total,
            page=page,
            size=size
        )

    @staticmethod
    def get_conversation(
        auth_user_id: str,
        conversation_id: str,
        use_case: GetConversationUseCase,
    ) -> ConversationResponse:
        conversation = use_case.execute(
            GetConversationQuery(conversation_id=conversation_id, auth_user_id=auth_user_id)
        )
        return ChatViewMapper.detail(conversation)

    @staticmethod
    def update_conversation(
        auth_user_id: str,
        conversation_id: str,
        request: UpdateConversationRequest,
        use_case: UpdateConversationUseCase,
    ) -> None:
        use_case.execute(
            UpdateConversationCommand(conversation_id=conversation_id, auth_user_id=auth_user_id, title=request.title)
        )

    @staticmethod
    def delete_conversation(
        auth_user_id: str,
        conversation_id: str,
        use_case: DeleteConversationUseCase,
    ) -> None:
        use_case.execute(
            DeleteConversationCommand(conversation_id=conversation_id, auth_user_id=auth_user_id)
        )

    @staticmethod
    def list_messages(
        auth_user_id: str,
        conversation_id: str,
        page: int,
        size: int,
        use_case: ListMessagesUseCase,
    ) -> Page[MessageResponse]:
        messages, total = use_case.execute(
            ListMessagesQuery(conversation_id=conversation_id, auth_user_id=auth_user_id, page=page, size=size)
        )
        return Page.create(
            items=[ChatViewMapper.message(m) for m in messages],
            total=total,
            page=page,
            size=size
        )

    @staticmethod
    def send_message(
        auth_user_id: str,
        conversation_id: str,
        request: SendMessageRequest,
        use_case: SendMessageUseCase,
    ) -> SendMessageResponse:
        result = use_case.execute(
            SendMessageCommand(
                conversation_id=conversation_id, auth_user_id=auth_user_id, content=request.content
            )
        )
        return ChatViewMapper.send_result(result)

    @staticmethod
    def stream_message(
        auth_user_id: str,
        conversation_id: str,
        request: SendMessageRequest,
        use_case: SendMessageUseCase,
    ) -> Iterator[str]:
        """Yield Server-Sent Events: one `token` event per chunk, then `done`."""
        command = SendMessageCommand(
            conversation_id=conversation_id, auth_user_id=auth_user_id, content=request.content
        )
        
        # Eagerly call execute_stream to catch any validation errors synchronously
        # before the StreamingResponse starts.
        stream_iterator = use_case.execute_stream(command)
        
        def _stream() -> Iterator[str]:
            for chunk in stream_iterator:
                yield _sse("token", {"content": chunk})
            yield _sse("done", {"conversation_id": conversation_id})
            
        return _stream()


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"
