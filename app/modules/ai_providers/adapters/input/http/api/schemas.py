from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional, Any, Dict, List
from app.modules.ai_providers.domain.value_objects.model_capability import ModelCapability

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
    
    capabilities: List[ModelCapability]
    
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

class AIProviderResponse(BaseModel):
    id: uuid.UUID
    name: str
    display_name: str
    description: Optional[str]
    api_base_url: str
    created_at: datetime
    updated_at: datetime
    models: List[AIModelResponse]=[]
