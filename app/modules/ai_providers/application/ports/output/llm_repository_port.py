from abc import ABC, abstractmethod
from typing import Any, Dict, List

from app.modules.ai_providers.domain.entities.ai_model import AIModel
from app.modules.chat.domain.entities.message import Message

class LLMClientPort(ABC):
    """
    Interface for communicating with external LLM APIs (OpenAI, Anthropic, Gemini, etc.).
    Note: This is a 'Client' or 'Gateway' port, not a 'Repository', because we 
    are communicating with an external service, not saving/loading from our own database.
    """
    
    @abstractmethod
    async def generate_text(self, model: AIModel, api_key: str, messages: List[Message]) -> str:
        """
        Sends a conversation to the LLM and gets a text response back.
        """
        pass
        
    @abstractmethod
    async def generate_structured_output(
        self, 
        model: AIModel, 
        api_key: str, 
        messages: List[Message], 
        schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Requests JSON/Structured output from the LLM based on a JSON schema.
        Used for Tool Calling (Phase 2).
        """
        pass
