from __future__ import annotations
from typing import Any
from app.modules.ai_providers.application.dto.provider_config_dto import ProviderConfigDTO
from app.modules.tools.application.ports.input.get_all_tools_use_case import GetAllToolsUseCase
from app.modules.chat.application.ports.output.agent_port import AgentPort
from app.modules.files.application.ports.output.file_repository_port import FileRepositoryPort
import uuid

from collections.abc import Iterator
import logging

logger = logging.getLogger(__name__)

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
from app.modules.ai_providers.application.ports.input.get_provider_config_use_case import GetProviderConfigUseCase
from app.modules.chat.domain.entities.conversation import Conversation
from app.modules.chat.domain.entities.message import Message
from app.modules.chat.domain.exceptions.chat_exceptions import (
    ConversationNotFound,
    EmptyMessageContent,
    ProviderConfigurationNotFound,
    ModelCapabilityError,
)
from app.modules.chat.application.dto.conversation_dto import ConversationDTO
from app.modules.chat.application.dto.message_dto import MessageDTO


_EMPTY_REPLY_FALLBACK = "(no response)"



class SendMessageHandler(SendMessageUseCase):
    """Handles `SendMessageCommand`: record the user turn, ask the LLM, record
    the assistant turn, and persist the whole aggregate.

    Depends exclusively on output ports (repository, LLM) — never on concrete
    adapters. That dependency inversion keeps the hexagon's core IO-free.
    """

    def __init__(
        self, 
        repository: ConversationRepositoryPort, 
        agent_port: AgentPort,
        get_provider_config: GetProviderConfigUseCase,
        get_all_tools: GetAllToolsUseCase | None = None,
        file_repo: FileRepositoryPort | None = None
    ) -> None:
        self._repository = repository
        self._agent_port = agent_port
        self._get_provider_config = get_provider_config
        self._get_all_tools = get_all_tools
        self._file_repo = file_repo


    def execute(self, command: SendMessageCommand) -> SendMessageResult:
        content = self._clean(command.content)
        conversation, user_message, config, tools, system_prompt = self._prepare_execution(command, content)

        reply, reasoning = self._agent_port.run_graph(
            history=conversation.messages,
            config=config,
            thinking_enabled=command.thinking_enabled,
            system_prompt=system_prompt,
            tools=tools
        )
        if not reply:
            reply = ""
        
        assistant_message = conversation.post_assistant_message(
            reply.strip() or _EMPTY_REPLY_FALLBACK
        )
        self._repository.save(conversation)

        return SendMessageResult(
            conversation=ConversationDTO.from_entity(conversation),
            user_message=MessageDTO.from_entity(user_message),
            assistant_message=MessageDTO.from_entity(assistant_message),
            reasoning=reasoning,
        )

    def execute_stream(self, command: SendMessageCommand) -> Iterator[tuple[str, str]]:
        content = self._clean(command.content)
        conversation, _, config, tools, system_prompt = self._prepare_execution(command, content)
        
        if not config.supports_stream:
            raise ModelCapabilityError("streaming")

        def _stream() -> Iterator[tuple[str, str]]:
            chunks: list[str] = []
            reasoning_chunks: list[str] = []
            for chunk_type, chunk_content in self._agent_port.stream_graph(
                history=conversation.messages,
                config=config,
                thinking_enabled=command.thinking_enabled,
                system_prompt=system_prompt,
                tools=tools
            ):
                if not chunk_content:
                    continue
                if chunk_type == "content":
                    chunks.append(chunk_content)
                elif chunk_type == "thinking":
                    reasoning_chunks.append(chunk_content)
                yield chunk_type, chunk_content

            reply = "".join(chunks).strip() or _EMPTY_REPLY_FALLBACK
            conversation.post_assistant_message(reply)
            self._repository.save(conversation)
            
        return _stream()

    # --- helpers -----------------------------------------------------------
    def _prepare_execution(
        self, command: SendMessageCommand, content: str
    ) -> tuple[Conversation, Message, ProviderConfigDTO, list[Any], str]:
        conversation = self._require(command.conversation_id, command.auth_user_id)
        
        config = self._get_provider_config.execute(command.provider_id, command.model_id)
        if not config:
            raise ProviderConfigurationNotFound(command.provider_id, command.model_id)
            
        user_message = conversation.post_user_message(content)
        
        tools = list(self._get_all_tools.execute(command.auth_user_id, command.file_id)) if self._get_all_tools else []
        self._validate_capabilities(command, config, tools)
        
        system_prompt = "You are a helpful assistant."
        if command.file_id and self._file_repo:
            file_entity = self._file_repo.get(command.file_id)
            if file_entity:
                from app.modules.files.domain.enums.file_status import FileStatus
                
                status_warning = ""
                if file_entity.status != FileStatus.PARSED:
                    status_warning = (
                        f"\n\nNOTE: The file is currently being processed by the system (Status: {file_entity.status.value}). "
                        f"You CAN answer questions about the file's metadata (name, type, size) using the context above. "
                        f"HOWEVER, if the user asks about the file's CONTENTS, you must inform them that the file is still processing and they should wait."
                    )
                    
                system_prompt += (
                    f"\n\n[ATTACHED FILE CONTEXT]\n"
                    f"The user has attached a file to this conversation.\n"
                    f"- File Name: {file_entity.original_filename}\n"
                    f"- Mime Type: {file_entity.mime_type}\n"
                    f"- Size: {file_entity.size_bytes} bytes\n"
                    f"{status_warning}\n\n"
                    f"IMPORTANT INSTRUCTION: If the user asks ANY question about the file "
                    f"(like what type of file it is, its name, or its contents), you MUST use this context. "
                    f"If they ask about its contents, you MUST use the `search_document` tool. Do NOT guess."
                )
            else:
                print(f"WARNING: File {command.file_id} not found in DB")
        else:
            print(f"WARNING: file_id={command.file_id}, file_repo={self._file_repo}")
                
        print(f"Final System Prompt: {system_prompt}")
        return conversation, user_message, config, tools, system_prompt

    def _validate_capabilities(self, command: SendMessageCommand, config: ProviderConfigDTO, tools: list[Any]) -> None:
        """Validates that the selected model supports the requested features."""
        if command.thinking_enabled and not config.supports_reasoning:
            raise ModelCapabilityError("reasoning/thinking")
            
        if tools and not config.supports_tools:
            raise ModelCapabilityError("tool calling")

    def _clean(self, content: str | None) -> str:
        cleaned = (content or "").strip()
        if not cleaned:
            raise EmptyMessageContent()
        return cleaned

    def _require(self, conversation_id: uuid.UUID, auth_user_id: uuid.UUID) -> Conversation:
        conversation = self._repository.get(conversation_id)
        if conversation is None or conversation.auth_user_id != auth_user_id:
            raise ConversationNotFound(conversation_id)
        return conversation
