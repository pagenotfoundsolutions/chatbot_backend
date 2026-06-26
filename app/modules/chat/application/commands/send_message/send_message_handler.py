from __future__ import annotations
import uuid

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
from app.modules.ai_providers.application.ports.input.get_provider_config_use_case import GetProviderConfigUseCase
from app.modules.chat.application.ports.output.llm_port import LLMPort
from app.modules.chat.domain.entities.conversation import Conversation
from app.modules.chat.domain.exceptions.chat_exceptions import (
    ConversationNotFound,
    EmptyMessageContent,
    ProviderConfigurationNotFound,
    RAGRetrievalFailed,
)
from app.modules.chat.application.dto.conversation_dto import ConversationDTO
from app.modules.chat.application.dto.message_dto import MessageDTO
from app.modules.rag.application.ports.input.search_chunks_use_case import SearchChunksUseCase

_EMPTY_REPLY_FALLBACK = "(no response)"


from app.modules.chat.domain.value_objects.message_role import MessageRole

class SendMessageHandler(SendMessageUseCase):
    """Handles `SendMessageCommand`: record the user turn, ask the LLM, record
    the assistant turn, and persist the whole aggregate.

    Depends exclusively on output ports (repository, LLM) — never on concrete
    adapters. That dependency inversion keeps the hexagon's core IO-free.
    """

    def __init__(
        self, 
        repository: ConversationRepositoryPort, 
        llm: LLMPort,
        get_provider_config: GetProviderConfigUseCase,
        search_chunks: SearchChunksUseCase | None = None
    ) -> None:
        self._repository = repository
        self._llm = llm
        self._get_provider_config = get_provider_config
        self._search_chunks = search_chunks

    def _rewrite_query(self, command: SendMessageCommand, conversation: Conversation, config) -> str:
        """Uses the LLM to rewrite the user's latest query based on conversation history into a standalone search query."""
        if not conversation.messages:
            return command.content
            
        history_str = "\n".join([f"{msg.role.value}: {msg.content}" for msg in conversation.messages[-5:]]) # Last 5 messages
        
        system_prompt = (
            "You are a search query rewriting assistant. Your goal is to convert the user's latest message "
            "into a highly optimized, standalone search query for a document retrieval system. "
            "Analyze the conversation history to resolve any pronouns (it, they, this) or missing context in the latest message. "
            "Return ONLY the rewritten search query string without quotes or explanations."
        )
        
        user_prompt = f"Conversation History:\n{history_str}\n\nLatest User Message: {command.content}\n\nRewritten Query:"
        
        from app.modules.chat.domain.entities.message import Message
        
        rewrite_messages = [
            Message.create(MessageRole.SYSTEM, system_prompt),
            Message.create(MessageRole.USER, user_prompt)
        ]
        
        try:
            rewritten = self._llm.generate(rewrite_messages, config)
            return rewritten.strip() if rewritten else command.content
        except Exception as e:
            print(f"Query rewriting failed: {e}")
            return command.content

    def _get_rag_context(self, command: SendMessageCommand, conversation: Conversation, config) -> str:
        if not self._search_chunks:
            return ""
            
        # Rewrite query to add context from history
        rewritten_query = self._rewrite_query(command, conversation, config)
        print(f"Original Query: {command.content} -> Rewritten for Search: {rewritten_query}")
        
        from app.modules.rag.application.queries.search_chunks.search_chunks_query import SearchChunksQuery
        query = SearchChunksQuery(
            text=rewritten_query,
            auth_user_id=command.auth_user_id,
            file_id=command.file_id,
            top_k=3
        )
        try:
            chunks = self._search_chunks.execute(query)
            if chunks:
                context_str = "\n\n".join([f"Document Chunk:\n{c.content}" for c in chunks])
                return f"Here is some relevant context from the user's documents. Use it to answer their question if applicable:\n\n{context_str}"
        except Exception as e:
            # Propagate error as a proper domain exception
            raise RAGRetrievalFailed(str(e))
        return ""

    def execute(self, command: SendMessageCommand) -> SendMessageResult:
        content = self._clean(command.content)
        conversation = self._require(command.conversation_id, command.auth_user_id)
        
        config = self._get_provider_config.execute(command.provider_id, command.model_id)
        if not config:
            raise ProviderConfigurationNotFound(command.provider_id, command.model_id)

        user_message = conversation.post_user_message(content)
        
        # Inject RAG context dynamically without saving it to DB
        messages_for_llm = list(conversation.messages)
        rag_context = self._get_rag_context(command, conversation, config)
        
        from app.modules.chat.domain.entities.message import Message
        
        if rag_context:
            messages_for_llm.insert(0, Message.create(MessageRole.SYSTEM, rag_context))

        reply = self._llm.generate(messages_for_llm, config) or ""
        assistant_message = conversation.post_assistant_message(
            reply.strip() or _EMPTY_REPLY_FALLBACK
        )
        self._repository.save(conversation)

        return SendMessageResult(
            conversation=ConversationDTO.from_entity(conversation),
            user_message=MessageDTO.from_entity(user_message),
            assistant_message=MessageDTO.from_entity(assistant_message),
        )

    def execute_stream(self, command: SendMessageCommand) -> Iterator[str]:
        content = self._clean(command.content)
        conversation = self._require(command.conversation_id, command.auth_user_id)
        
        config = self._get_provider_config.execute(command.provider_id, command.model_id)
        if not config:
            raise ProviderConfigurationNotFound(command.provider_id, command.model_id)
            
        conversation.post_user_message(content)
        
        # Inject RAG context dynamically without saving it to DB
        messages_for_llm = list(conversation.messages)
        rag_context = self._get_rag_context(command, conversation, config)
        
        from app.modules.chat.domain.entities.message import Message
        
        if rag_context:
            messages_for_llm.insert(0, Message.create(MessageRole.SYSTEM, rag_context))

        def _stream() -> Iterator[str]:
            chunks: list[str] = []
            for chunk in self._llm.stream(messages_for_llm, config):
                if not chunk:
                    continue
                chunks.append(chunk)
                yield chunk

            reply = "".join(chunks).strip() or _EMPTY_REPLY_FALLBACK
            conversation.post_assistant_message(reply)
            self._repository.save(conversation)
            
        return _stream()

    # --- helpers -----------------------------------------------------------
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
