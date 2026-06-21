from __future__ import annotations
import uuid

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import StreamingResponse
from uuid import UUID

from app.shared.security.dependencies import get_current_user_id
from app.shared.pagination import Page
from app.modules.chat.adapters.input.http.controller import ChatController
from app.modules.chat.adapters.input.http.dependencies import (
    get_create_conversation_use_case,
    get_get_conversation_use_case,
    get_list_conversations_use_case,
    get_send_message_use_case,
    get_delete_conversation_use_case,
    get_list_messages_use_case,
    get_update_conversation_use_case,
)
from app.modules.chat.adapters.input.http.schemas import (
    ConversationResponse,
    ConversationSummaryResponse,
    MessageResponse,
    CreateConversationRequest,
    UpdateConversationRequest,
    SendMessageRequest,
    SendMessageResponse,
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
    auth_user_id: UUID = Depends(get_current_user_id),
) -> SuccessResp[ConversationResponse]:
    return SuccessResp(
        message="Conversation created",
        data=ChatController.create_conversation(auth_user_id, request, use_case),
    )


@router.get("", response_model=SuccessResp[Page[ConversationSummaryResponse]])
def list_conversations(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=1000),
    use_case: ListConversationsUseCase = Depends(get_list_conversations_use_case),
    auth_user_id: UUID = Depends(get_current_user_id),
) -> SuccessResp[Page[ConversationSummaryResponse]]:
    return SuccessResp(
        message="Conversations fetched",
        data=ChatController.list_conversations(auth_user_id, page, size, use_case),
    )


@router.get("/{conversation_id}", response_model=SuccessResp[ConversationResponse])
def get_conversation(
    conversation_id: uuid.UUID,
    use_case: GetConversationUseCase = Depends(get_get_conversation_use_case),
    auth_user_id: UUID = Depends(get_current_user_id),
) -> SuccessResp[ConversationResponse]:
    return SuccessResp(
        message="Conversation fetched",
        data=ChatController.get_conversation(auth_user_id, conversation_id, use_case),
    )


@router.put("/{conversation_id}", response_model=SuccessResp[None])
def update_conversation(
    conversation_id: uuid.UUID,
    request: UpdateConversationRequest,
    use_case: UpdateConversationUseCase = Depends(get_update_conversation_use_case),
    auth_user_id: UUID = Depends(get_current_user_id),
) -> SuccessResp[None]:
    ChatController.update_conversation(auth_user_id, conversation_id, request, use_case)
    return SuccessResp(
        message="Conversation updated successfully",
        data=None,
    )


@router.delete("/{conversation_id}", response_model=SuccessResp[None])
def delete_conversation(
    conversation_id: uuid.UUID,
    use_case: DeleteConversationUseCase = Depends(get_delete_conversation_use_case),
    auth_user_id: UUID = Depends(get_current_user_id),
) -> SuccessResp[None]:
    ChatController.delete_conversation(auth_user_id, conversation_id, use_case)
    return SuccessResp(
        message="Conversation deleted successfully",
        data=None,
    )


@router.get("/{conversation_id}/messages", response_model=SuccessResp[Page[MessageResponse]])
def list_messages(
    conversation_id: uuid.UUID,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    use_case: ListMessagesUseCase = Depends(get_list_messages_use_case),
    auth_user_id: UUID = Depends(get_current_user_id),
) -> SuccessResp[Page[MessageResponse]]:
    return SuccessResp(
        message="Messages fetched",
        data=ChatController.list_messages(auth_user_id, conversation_id, page, size, use_case),
    )


@router.post(
    "/{conversation_id}/messages",
    response_model=SuccessResp[SendMessageResponse],
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    conversation_id: uuid.UUID,
    request: SendMessageRequest,
    use_case: SendMessageUseCase = Depends(get_send_message_use_case),
    auth_user_id: UUID = Depends(get_current_user_id),
) -> SuccessResp[SendMessageResponse]:
    return SuccessResp(
        message="Message sent",
        data=ChatController.send_message(auth_user_id, conversation_id, request, use_case),
    )


@router.post("/{conversation_id}/messages/stream")
def stream_message(
    conversation_id: uuid.UUID,
    request: SendMessageRequest,
    use_case: SendMessageUseCase = Depends(get_send_message_use_case),
    auth_user_id: UUID = Depends(get_current_user_id),
) -> StreamingResponse:
    """Stream the assistant reply as Server-Sent Events (text/event-stream)."""
    return StreamingResponse(
        ChatController.stream_message(auth_user_id, conversation_id, request, use_case),
        media_type="text/event-stream",
    )
