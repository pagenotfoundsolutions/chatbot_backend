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
from app.modules.chat.application.services.cancellation_registry import StreamCancellationRegistry


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

        reply, thinking_content = self._agent_port.run_graph(
            history=conversation.messages,
            config=config,
            thinking_enabled=command.thinking_enabled,
            system_prompt=system_prompt,
            tools=tools
        )
        if not reply:
            reply = ""
        
        assistant_message = conversation.post_assistant_message(
            reply.strip() or _EMPTY_REPLY_FALLBACK,
            thinking_content=thinking_content
        )
        self._repository.save(conversation)

        return SendMessageResult(
            conversation=ConversationDTO.from_entity(conversation),
            user_message=MessageDTO.from_entity(user_message),
            assistant_message=MessageDTO.from_entity(assistant_message),
            thinking_content=thinking_content,
        )

    def execute_stream(self, command: SendMessageCommand) -> Iterator[tuple[str, str]]:
        content = self._clean(command.content)
        conversation, _, config, tools, system_prompt = self._prepare_execution(command, content)
        
        if not config.supports("stream"):
            raise ModelCapabilityError("streaming")

        def _stream() -> Iterator[tuple[str, str]]:
            StreamCancellationRegistry.clear(command.conversation_id)
            chunks: list[str] = []
            reasoning_chunks: list[str] = []
            try:
                for chunk_type, chunk_content in self._agent_port.stream_graph(
                    history=conversation.messages,
                    config=config,
                    thinking_enabled=command.thinking_enabled,
                    system_prompt=system_prompt,
                    tools=tools
                ):
                    if StreamCancellationRegistry.is_cancelled(command.conversation_id):
                        logger.info(f"Stream cancelled for conversation {command.conversation_id}")
                        break
                        
                    if not chunk_content:
                        continue
                    if chunk_type == "content":
                        chunks.append(chunk_content)
                    elif chunk_type == "thinking":
                        reasoning_chunks.append(chunk_content)
                    yield chunk_type, chunk_content
            finally:
                StreamCancellationRegistry.clear(command.conversation_id)
                reply = "".join(chunks).strip() or _EMPTY_REPLY_FALLBACK
                reasoning = "".join(reasoning_chunks).strip() or None
                conversation.post_assistant_message(reply, thinking_content=reasoning)
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
            
        user_message = conversation.post_user_message(content=command.content, file_id=command.file_id)
        
        if command.file_id:
            conversation.attach_file(command.file_id)

        active_file_ids = conversation.file_ids

        tools = list(self._get_all_tools.execute(command.auth_user_id, active_file_ids)) if self._get_all_tools else []
        if not config.supports("tools"):
            tools = []
            
        self._validate_capabilities(command, config, tools)
        
        system_prompt = "You are a helpful assistant."
        if active_file_ids and self._file_repo:
            file_contexts = []
            # Optimization: Fetch all file entities in a single query
            file_entities = self._file_repo.get_many_by_ids(list(active_file_ids))
            
            # Create a quick lookup map by ID (to check missing files)
            found_files_map = {entity.id: entity for entity in file_entities}
            
            for fid in active_file_ids:
                file_entity = found_files_map.get(fid)
                if file_entity:
                    from app.modules.files.domain.enums.file_status import FileStatus
                    
                    status_warning = ""
                    if file_entity.status != FileStatus.PARSED:
                        status_warning = (
                            f"\nNOTE: The file is currently being processed by the system (Status: {file_entity.status.value}). "
                            f"You CAN answer questions about the file's metadata (name, type, size) using the context above. "
                            f"HOWEVER, if the user asks about the file's CONTENTS, you must inform them that the file is still processing and they should wait."
                        )
                    file_contexts.append(
                        f"- File Name: {file_entity.original_filename}\n"
                        f"- Mime Type: {file_entity.mime_type}\n"
                        f"- Size: {file_entity.size_bytes} bytes"
                        f"{status_warning}"
                    )
                else:
                    logger.warning(f"File {fid} not found in DB")
            
            if file_contexts:
                system_prompt += (
                    f"\n\n[ATTACHED FILES CONTEXT]\n"
                    f"The user has attached the following files to this conversation:\n\n"
                    + "\n\n".join(file_contexts) +
                    f"\n\nIMPORTANT INSTRUCTION: If the user asks ANY question about these files "
                    f"(like what type they are, their names, or their contents), you MUST use this context. "
                    f"If they ask about their contents, you MUST use the `search_document` tool. Do NOT guess."
                )
        return conversation, user_message, config, tools, system_prompt

    def _validate_capabilities(self, command: SendMessageCommand, config: ProviderConfigDTO, tools: list[Any]) -> None:
        """Validates that the selected model supports the requested features."""
        if command.thinking_enabled and not config.supports("reasoning"):
            raise ModelCapabilityError("reasoning/thinking")
            
        # We don't raise an error for tools. If a model doesn't support tools, 
        # we just won't pass them to the graph.

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
