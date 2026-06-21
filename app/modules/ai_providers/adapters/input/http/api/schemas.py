from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional, Any, Dict, List

class AIProviderResponse(BaseModel):
    id: uuid.UUID
    name: str
    display_name: str
    description: Optional[str]
    api_base_url: str
    created_at: datetime
    updated_at: datetime

class AIModelResponse(BaseModel):
    id: uuid.UUID
    provider_id: uuid.UUID
    model_key: str
    display_name: str
    description: Optional[str]
    is_active: bool
    is_default: bool
    is_deprecated: bool
    model_type: str
    
    max_input_tokens: int
    max_output_tokens: int
    max_context_window: int
    
    default_temperature: float
    default_top_p: float
    default_frequency_penalty: float
    default_presence_penalty: float
    
    supports_tools: bool
    supports_parallel_tools: bool
    supports_structured_output: bool
    supports_json: bool
    supports_stream: bool
    supports_vision: bool
    supports_image_generation: bool
    supports_audio_input: bool
    supports_audio_output: bool
    supports_embeddings: bool
    supports_reasoning: bool
    supports_system_prompt: bool
    supports_web_search: bool
    supports_file_upload: bool
    supports_pdf: bool
    supports_function_call: bool
    supports_seed: bool
    supports_response_format: bool
    supports_cache: bool
    supports_citations: bool
    supports_multimodal: bool
    
    typical_latency_ms: int
    speed_tier: str
    input_price_per_million: float
    output_price_per_million: float
    cache_price_per_million: float
    priority: int
    
    fallback_model_id: Optional[uuid.UUID]
    provider_model_name: Optional[str]
    api_version: Optional[str]
    endpoint: Optional[str]
    extra: Optional[Dict[str, Any]]
    
    created_at: datetime
    updated_at: datetime
