from __future__ import annotations

from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.modules.chat.adapters.output.llm.echo_llm_adapter import EchoLLMAdapter
from app.modules.chat.adapters.output.persistence.sqlalchemy_conversation_repository import (
    SqlAlchemyConversationRepository,
)
from app.modules.chat.application.commands.create_conversation.create_conversation_handler import (
    CreateConversationHandler,
)
from app.modules.chat.application.commands.delete_conversation.delete_conversation_handler import (
    DeleteConversationHandler,
)
from app.modules.chat.application.commands.update_conversation.update_conversation_handler import (
    UpdateConversationHandler,
)
from app.modules.chat.application.commands.send_message.send_message_handler import (
    SendMessageHandler,
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
from app.modules.chat.application.ports.output.conversation_repository_port import (
    ConversationRepositoryPort,
)
from app.modules.chat.application.ports.output.llm_port import LLMPort
from app.modules.chat.application.queries.get_conversation.get_conversation_handler import (
    GetConversationHandler,
)
from app.modules.chat.application.queries.list_conversations.list_conversations_handler import (
    ListConversationsHandler,
)
from app.modules.chat.application.queries.list_messages.list_messages_handler import (
    ListMessagesHandler,
)
from app.modules.chat.infrastructure.config.chat_config import get_chat_config
from app.shared.database.session import get_db

# Composition root for the chat hexagon: the single place that binds abstract
# ports to concrete adapters. To go from echo-stub to a real provider, set
# LLM_PROVIDER in .env — nothing here changes.


@lru_cache
def get_llm() -> LLMPort:
    """Build the LLM adapter once (singleton) from config."""
    config = get_chat_config()
    
    if config.provider.lower() == "echo":
        from app.modules.chat.adapters.output.llm.echo_llm_adapter import EchoLLMAdapter
        return EchoLLMAdapter()

    from app.modules.chat.adapters.output.llm.nvidia_llm_adapter import NvidiaLLMAdapter
    return NvidiaLLMAdapter(config)


def get_conversation_repository(
    db: Session = Depends(get_db),
) -> ConversationRepositoryPort:
    return SqlAlchemyConversationRepository(db)


def get_create_conversation_use_case(
    repository: ConversationRepositoryPort = Depends(get_conversation_repository),
) -> CreateConversationUseCase:
    return CreateConversationHandler(repository)


def get_send_message_use_case(
    repository: ConversationRepositoryPort = Depends(get_conversation_repository),
    llm: LLMPort = Depends(get_llm),
) -> SendMessageUseCase:
    return SendMessageHandler(repository=repository, llm=llm)


def get_get_conversation_use_case(
    repository: ConversationRepositoryPort = Depends(get_conversation_repository),
) -> GetConversationUseCase:
    return GetConversationHandler(repository)


def get_list_conversations_use_case(
    repository: ConversationRepositoryPort = Depends(get_conversation_repository),
) -> ListConversationsUseCase:
    return ListConversationsHandler(repository)


def get_delete_conversation_use_case(
    repository: ConversationRepositoryPort = Depends(get_conversation_repository),
) -> DeleteConversationUseCase:
    return DeleteConversationHandler(repository)


def get_list_messages_use_case(
    repository: ConversationRepositoryPort = Depends(get_conversation_repository),
) -> ListMessagesUseCase:
    return ListMessagesHandler(repository)


def get_update_conversation_use_case(
    repository: ConversationRepositoryPort = Depends(get_conversation_repository),
) -> UpdateConversationUseCase:
    return UpdateConversationHandler(repository)
