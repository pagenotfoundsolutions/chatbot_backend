from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence, Any, Iterator
from app.modules.chat.domain.entities.message import Message
from app.modules.ai_providers.application.dto.provider_config_dto import ProviderConfigDTO

class AgentPort(ABC):
    """Output port for Agentic Graph Orchestration.
    
    This port abstracts the LangGraph execution away from the domain.
    """
    @abstractmethod
    def run_graph(
        self, 
        history: Sequence[Message], 
        config: ProviderConfigDTO,
        thinking_enabled: bool,
        system_prompt: str,
        tools: list[Any]
    ) -> tuple[str, str | None]:
        pass

    @abstractmethod
    def stream_graph(
        self, 
        history: Sequence[Message], 
        config: ProviderConfigDTO,
        thinking_enabled: bool,
        system_prompt: str,
        tools: list[Any]
    ) -> Iterator[tuple[str, str]]:
        pass
