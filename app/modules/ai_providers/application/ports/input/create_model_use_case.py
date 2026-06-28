import uuid
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
from app.modules.ai_providers.domain.entities.ai_model import AIModel
from app.modules.ai_providers.domain.value_objects.model_capability import ModelCapability

class CreateModelCommand:
    def __init__(
        self,
        provider_id: uuid.UUID,
        model_key: str,
        display_name: str,
        description: Optional[str] = None,
        is_active: bool = True,
        is_default: bool = False,
        is_deprecated: bool = False,
        model_type: str = "text",
        
        max_input_tokens: int = 8192,
        max_output_tokens: int = 4096,
        max_context_window: int = 8192,
        
        default_temperature: float = 0.7,
        default_top_p: float = 1.0,
        default_frequency_penalty: float = 0.0,
        default_presence_penalty: float = 0.0,
        
        capabilities: Optional[List[ModelCapability]] = None,
        
        typical_latency_ms: int = 1000,
        speed_tier: str = "standard",
        input_price_per_million: float = 0.0,
        output_price_per_million: float = 0.0,
        cache_price_per_million: float = 0.0,
        priority: int = 0,
        
        fallback_model_id: Optional[uuid.UUID] = None,
        provider_model_name: Optional[str] = None,
        api_version: Optional[str] = None,
        endpoint: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        self.provider_id = provider_id
        self.model_key = model_key
        self.display_name = display_name
        self.description = description
        
        self.is_active = is_active
        self.is_default = is_default
        self.is_deprecated = is_deprecated
        self.model_type = model_type
        
        self.max_input_tokens = max_input_tokens
        self.max_output_tokens = max_output_tokens
        self.max_context_window = max_context_window
        
        self.default_temperature = default_temperature
        self.default_top_p = default_top_p
        self.default_frequency_penalty = default_frequency_penalty
        self.default_presence_penalty = default_presence_penalty
        
        self.capabilities = [ModelCapability(c) if isinstance(c, str) else c for c in capabilities] if capabilities is not None else []
        
        self.typical_latency_ms = typical_latency_ms
        self.speed_tier = speed_tier
        self.input_price_per_million = input_price_per_million
        self.output_price_per_million = output_price_per_million
        self.cache_price_per_million = cache_price_per_million
        self.priority = priority
        
        self.fallback_model_id = fallback_model_id
        self.provider_model_name = provider_model_name
        self.api_version = api_version
        self.endpoint = endpoint
        self.extra = extra

class CreateModelUseCase(ABC):
    @abstractmethod
    def execute(self, command: CreateModelCommand) -> AIModel:
        pass
