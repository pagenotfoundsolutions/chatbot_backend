import uuid
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from app.modules.ai_providers.domain.entities.ai_model import AIModel

class UpdateModelCommand:
    def __init__(
        self,
        id: uuid.UUID,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_default: Optional[bool] = None,
        is_deprecated: Optional[bool] = None,
        model_type: Optional[str] = None,
        
        max_input_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        max_context_window: Optional[int] = None,
        
        default_temperature: Optional[float] = None,
        default_top_p: Optional[float] = None,
        default_frequency_penalty: Optional[float] = None,
        default_presence_penalty: Optional[float] = None,
        
        supports_tools: Optional[bool] = None,
        supports_parallel_tools: Optional[bool] = None,
        supports_structured_output: Optional[bool] = None,
        supports_json: Optional[bool] = None,
        supports_stream: Optional[bool] = None,
        supports_vision: Optional[bool] = None,
        supports_image_generation: Optional[bool] = None,
        supports_audio_input: Optional[bool] = None,
        supports_audio_output: Optional[bool] = None,
        supports_embeddings: Optional[bool] = None,
        supports_reasoning: Optional[bool] = None,
        supports_system_prompt: Optional[bool] = None,
        supports_web_search: Optional[bool] = None,
        supports_file_upload: Optional[bool] = None,
        supports_pdf: Optional[bool] = None,
        supports_function_call: Optional[bool] = None,
        supports_seed: Optional[bool] = None,
        supports_response_format: Optional[bool] = None,
        supports_cache: Optional[bool] = None,
        supports_citations: Optional[bool] = None,
        supports_multimodal: Optional[bool] = None,
        
        typical_latency_ms: Optional[int] = None,
        speed_tier: Optional[str] = None,
        input_price_per_million: Optional[float] = None,
        output_price_per_million: Optional[float] = None,
        cache_price_per_million: Optional[float] = None,
        priority: Optional[int] = None,
        
        fallback_model_id: Optional[uuid.UUID] = None,
        provider_model_name: Optional[str] = None,
        api_version: Optional[str] = None,
        endpoint: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        self.id = id
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
        
        self.supports_tools = supports_tools
        self.supports_parallel_tools = supports_parallel_tools
        self.supports_structured_output = supports_structured_output
        self.supports_json = supports_json
        self.supports_stream = supports_stream
        self.supports_vision = supports_vision
        self.supports_image_generation = supports_image_generation
        self.supports_audio_input = supports_audio_input
        self.supports_audio_output = supports_audio_output
        self.supports_embeddings = supports_embeddings
        self.supports_reasoning = supports_reasoning
        self.supports_system_prompt = supports_system_prompt
        self.supports_web_search = supports_web_search
        self.supports_file_upload = supports_file_upload
        self.supports_pdf = supports_pdf
        self.supports_function_call = supports_function_call
        self.supports_seed = supports_seed
        self.supports_response_format = supports_response_format
        self.supports_cache = supports_cache
        self.supports_citations = supports_citations
        self.supports_multimodal = supports_multimodal
        
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

class UpdateModelUseCase(ABC):
    @abstractmethod
    def execute(self, command: UpdateModelCommand) -> Optional[AIModel]:
        pass
