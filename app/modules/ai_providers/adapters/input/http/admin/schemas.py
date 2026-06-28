from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import uuid
from app.modules.ai_providers.domain.value_objects.model_capability import ModelCapability

# --- Provider Schemas ---

class CreateProviderRequest(BaseModel):
    name: str = Field(..., max_length=50, description="Unique internal identifier for the provider")
    display_name: str = Field(..., max_length=100, description="Human-readable name")
    description: Optional[str] = Field(None, max_length=500)
    api_base_url: str = Field(..., max_length=255)
    api_key: str = Field(..., max_length=255)

class UpdateProviderRequest(BaseModel):
    display_name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    api_base_url: Optional[str] = Field(None, max_length=255)
    api_key: Optional[str] = Field(None, max_length=255)

# --- Model Schemas ---

class CreateModelRequest(BaseModel):
    provider_id: uuid.UUID
    model_key: str = Field(..., max_length=100)
    display_name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    
    is_active: bool = True
    is_default: bool = False
    is_deprecated: bool = False
    model_type: str = "text"
    
    max_input_tokens: int = 8192
    max_output_tokens: int = 4096
    max_context_window: int = 8192
    
    default_temperature: float = 0.7
    default_top_p: float = 1.0
    default_frequency_penalty: float = 0.0
    default_presence_penalty: float = 0.0
    
    capabilities: Optional[List[ModelCapability]] = Field(default_factory=list)
    
    typical_latency_ms: int = 1000
    speed_tier: str = "standard"
    input_price_per_million: float = 0.0
    output_price_per_million: float = 0.0
    cache_price_per_million: float = 0.0
    priority: int = 0
    
    fallback_model_id: Optional[uuid.UUID] = None
    provider_model_name: Optional[str] = None
    api_version: Optional[str] = None
    endpoint: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None

class UpdateModelRequest(BaseModel):
    display_name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    is_deprecated: Optional[bool] = None
    model_type: Optional[str] = None
    
    max_input_tokens: Optional[int] = None
    max_output_tokens: Optional[int] = None
    max_context_window: Optional[int] = None
    
    default_temperature: Optional[float] = None
    default_top_p: Optional[float] = None
    default_frequency_penalty: Optional[float] = None
    default_presence_penalty: Optional[float] = None
    
    capabilities: Optional[List[ModelCapability]] = None
    
    typical_latency_ms: Optional[int] = None
    speed_tier: Optional[str] = None
    input_price_per_million: Optional[float] = None
    output_price_per_million: Optional[float] = None
    cache_price_per_million: Optional[float] = None
    priority: Optional[int] = None
    
    fallback_model_id: Optional[uuid.UUID] = None
    provider_model_name: Optional[str] = None
    api_version: Optional[str] = None
    endpoint: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None


