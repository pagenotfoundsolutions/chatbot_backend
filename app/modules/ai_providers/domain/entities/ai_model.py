from dataclasses import dataclass, field, InitVar
import uuid
from typing import Optional, Any
from datetime import datetime

from app.shared.kernel.aggregate_root import AggregateRoot
from app.modules.ai_providers.domain.value_objects.model_capability import ModelCapability

@dataclass(kw_only=True)
class AIModel(AggregateRoot[uuid.UUID]):
    id: InitVar[uuid.UUID]
    provider_id: uuid.UUID
    model_key: str
    display_name: str
    description: str
    
    # Defaults
    is_active: bool = True
    is_default: bool = False
    is_deprecated: bool = False
    model_type: str = "text"
    
    # Tokens & Limits
    max_input_tokens: int = 8192
    max_output_tokens: int = 4096
    max_context_window: int = 8192
    
    # Hyperparameters
    default_temperature: float = 0.7
    default_top_p: float = 1.0
    default_frequency_penalty: float = 0.0
    default_presence_penalty: float = 0.0
    
    # Capabilities
    capabilities: list[ModelCapability] = field(default_factory=list)
    
    # Pricing & Performance
    typical_latency_ms: int = 1000
    speed_tier: str = "standard"
    input_price_per_million: float = 0.0
    output_price_per_million: float = 0.0
    cache_price_per_million: float = 0.0
    priority: int = 0
    
    # Optional / Extra
    fallback_model_id: Optional[uuid.UUID] = None
    provider_model_name: Optional[str] = None
    api_version: Optional[str] = None
    endpoint: Optional[str] = None
    extra: Optional[dict[str, Any]] = None
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None

    def __post_init__(self, id: uuid.UUID):
        # Explicitly initialize the parent AggregateRoot (and Entity)
        # This securely sets self._id and initializes the DomainEvents array
        super().__init__(id)
