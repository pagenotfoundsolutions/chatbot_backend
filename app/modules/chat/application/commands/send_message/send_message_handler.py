from __future__ import annotations

from collections.abc import Iterator

from app.modules.chat.application.commands.send_message.send_message_command import (
    SendMessageCommand,
)
from app.modules.chat.application.dto.send_message_result import SendMessageResult
from app.modules.chat.application.ports.input.send_message_use_case import (
    SendMessageUseCase,
)
from app.modules.chat.application.ports.output.conversation_repository_port import (
    ConversationRepositoryPort,
)
from app.modules.chat.application.ports.output.llm_port import LLMPort
from app.modules.chat.domain.entities.conversation import Conversation
from app.modules.chat.domain.exceptions.chat_exceptions import (
    ConversationNotFound,
    EmptyMessageContent,
)

_EMPTY_REPLY_FALLBACK = "(no response)"


class SendMessageHandler(SendMessageUseCase):
    """Handles `SendMessageCommand`: record the user turn, ask the LLM, record
    the assistant turn, and persist the whole aggregate.

    Depends exclusively on output ports (repository, LLM) — never on concrete
    adapters. That dependency inversion keeps the hexagon's core IO-free.
    """

    def __init__(self, repository: ConversationRepositoryPort, llm: LLMPort) -> None:
        self._repository = repository
        self._llm = llm

    def execute(self, command: SendMessageCommand) -> SendMessageResult:
        content = self._clean(command.content)
        conversation = self._require(command.conversation_id, command.auth_user_id)

        user_message = conversation.post_user_message(content)
        reply = self._llm.generate(conversation.messages) or ""
        assistant_message = conversation.post_assistant_message(
            reply.strip() or _EMPTY_REPLY_FALLBACK
        )
        self._repository.save(conversation)

        return SendMessageResult(
            conversation=conversation,
            user_message=user_message,
            assistant_message=assistant_message,
        )

    def execute_stream(self, command: SendMessageCommand) -> Iterator[str]:
        content = self._clean(command.content)
        conversation = self._require(command.conversation_id, command.auth_user_id)
        conversation.post_user_message(content)

        chunks: list[str] = []
        for chunk in self._llm.stream(conversation.messages):
            if not chunk:
                continue
            chunks.append(chunk)
            yield chunk

        reply = "".join(chunks).strip() or _EMPTY_REPLY_FALLBACK
        conversation.post_assistant_message(reply)
        self._repository.save(conversation)

    # --- helpers -----------------------------------------------------------
    def _clean(self, content: str | None) -> str:
        cleaned = (content or "").strip()
        if not cleaned:
            raise EmptyMessageContent()
        return cleaned

    def _require(self, conversation_id: str, auth_user_id: str) -> Conversation:
        conversation = self._repository.get(conversation_id)
        if conversation is None or conversation.auth_user_id != auth_user_id:
            raise ConversationNotFound(conversation_id)
        return conversation
