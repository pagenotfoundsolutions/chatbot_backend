from __future__ import annotations

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from app.modules.chat.adapters.input.http.controller import ChatController
from app.modules.chat.adapters.input.http.dependencies import (
    get_create_conversation_use_case,
    get_get_conversation_use_case,
    get_list_conversations_use_case,
    get_send_message_use_case,
)
from app.modules.chat.adapters.input.http.schemas import (
    ConversationResponse,
    ConversationSummaryResponse,
    CreateConversationRequest,
    SendMessageRequest,
    SendMessageResponse,
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
from app.shared.resp import SuccessResp

# Inbound (driving) REST adapter. Thin: HTTP <-> use-case translation only.
router = APIRouter(prefix="/chats")


@router.post(
    "",
    response_model=SuccessResp[ConversationResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    request: CreateConversationRequest,
    use_case: CreateConversationUseCase = Depends(get_create_conversation_use_case),
) -> SuccessResp[ConversationResponse]:
    return SuccessResp(
        message="Conversation created",
        data=ChatController.create_conversation(request, use_case),
    )


@router.get("", response_model=SuccessResp[list[ConversationSummaryResponse]])
def list_conversations(
    use_case: ListConversationsUseCase = Depends(get_list_conversations_use_case),
) -> SuccessResp[list[ConversationSummaryResponse]]:
    return SuccessResp(
        message="Conversations fetched",
        data=ChatController.list_conversations(use_case),
    )


@router.get("/{conversation_id}", response_model=SuccessResp[ConversationResponse])
def get_conversation(
    conversation_id: str,
    use_case: GetConversationUseCase = Depends(get_get_conversation_use_case),
) -> SuccessResp[ConversationResponse]:
    return SuccessResp(
        message="Conversation fetched",
        data=ChatController.get_conversation(conversation_id, use_case),
    )


@router.post(
    "/{conversation_id}/messages",
    response_model=SuccessResp[SendMessageResponse],
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    conversation_id: str,
    request: SendMessageRequest,
    use_case: SendMessageUseCase = Depends(get_send_message_use_case),
) -> SuccessResp[SendMessageResponse]:
    return SuccessResp(
        message="Message sent",
        data=ChatController.send_message(conversation_id, request, use_case),
    )


@router.post("/{conversation_id}/messages/stream")
def stream_message(
    conversation_id: str,
    request: SendMessageRequest,
    use_case: SendMessageUseCase = Depends(get_send_message_use_case),
) -> StreamingResponse:
    """Stream the assistant reply as Server-Sent Events (text/event-stream)."""
    return StreamingResponse(
        ChatController.stream_message(conversation_id, request, use_case),
        media_type="text/event-stream",
    )
