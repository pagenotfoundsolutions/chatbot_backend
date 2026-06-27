from __future__ import annotations


from fastapi import Depends
from sqlalchemy.orm import Session

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
from app.shared.database.session import get_db

# Composition root for the chat hexagon: the single place that binds abstract
# ports to concrete adapters. To go from echo-stub to a real provider, set
# LLM_PROVIDER in .env — nothing here changes.


from app.modules.ai_providers.application.ports.input.get_provider_config_use_case import GetProviderConfigUseCase

def get_provider_config_use_case(db: Session = Depends(get_db)) -> GetProviderConfigUseCase:
    """Build the Use Case from ai_providers."""
    from app.modules.ai_providers.adapters.output.persistence.sqlalchemy_provider_repository import SqlAlchemyProviderRepository
    from app.modules.ai_providers.adapters.output.persistence.sqlalchemy_model_repository import SqlAlchemyModelRepository
    from app.modules.ai_providers.application.queries.get_provider_config.get_provider_config_handler import GetProviderConfigHandler
    
    provider_repo = SqlAlchemyProviderRepository(db)
    model_repo = SqlAlchemyModelRepository(db)
    
    return GetProviderConfigHandler(provider_repo, model_repo)

from app.modules.chat.application.ports.output.agent_port import AgentPort
from app.modules.tools.application.ports.input.get_all_tools_use_case import GetAllToolsUseCase
from app.modules.tools.adapters.input.http.dependencies import get_all_tools_use_case
from app.modules.files.adapters.input.http.api.dependencies import get_file_repository
from app.modules.files.application.ports.output.file_repository_port import FileRepositoryPort

def get_llm() -> LLMPort:
    """Build the dynamic LLM adapter."""
    from app.modules.chat.adapters.output.llm.dynamic_llm_adapter import DynamicLLMAdapter
    return DynamicLLMAdapter()

def get_agent_port() -> AgentPort:
    from app.modules.chat.adapters.output.agent.langgraph_agent_adapter import LangGraphAgentAdapter
    return LangGraphAgentAdapter()

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
    agent_port: AgentPort = Depends(get_agent_port),
    get_provider_config: GetProviderConfigUseCase = Depends(get_provider_config_use_case),
    get_all_tools: GetAllToolsUseCase = Depends(get_all_tools_use_case),
    file_repo: FileRepositoryPort = Depends(get_file_repository)
) -> SendMessageUseCase:
    return SendMessageHandler(
        repository=repository, 
        agent_port=agent_port, 
        get_provider_config=get_provider_config,
        get_all_tools=get_all_tools,
        file_repo=file_repo
    )


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
