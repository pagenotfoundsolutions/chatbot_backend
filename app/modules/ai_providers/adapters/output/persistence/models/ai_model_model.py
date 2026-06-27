from sqlalchemy import Column, String, Boolean, Float, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from app.shared.database.database import Base
from app.shared.database.core_model import CoreModelMixin

class AIModelModel(CoreModelMixin, Base):
    __tablename__ = "ai_models"

    provider_id = Column(PGUUID(as_uuid=True), ForeignKey("ai_providers.id"), nullable=False, index=True)
    model_key = Column(String(100), nullable=False, unique=True, index=True)
    display_name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    
    # Defaults
    is_active = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    is_deprecated = Column(Boolean, default=False, nullable=False)
    model_type = Column(String(50), default="text", nullable=False)
    
    # Tokens & Limits
    max_input_tokens = Column(Integer, default=8192, nullable=False)
    max_output_tokens = Column(Integer, default=4096, nullable=False)
    max_context_window = Column(Integer, default=8192, nullable=False)
    
    # Hyperparameters
    default_temperature = Column(Float, default=0.7, nullable=False)
    default_top_p = Column(Float, default=1.0, nullable=False)
    default_frequency_penalty = Column(Float, default=0.0, nullable=False)
    default_presence_penalty = Column(Float, default=0.0, nullable=False)
    
    # Capabilities (Supports)
    supports_tools = Column(Boolean, default=False, nullable=False)
    supports_parallel_tools = Column(Boolean, default=False, nullable=False)
    supports_structured_output = Column(Boolean, default=False, nullable=False)
    supports_json = Column(Boolean, default=False, nullable=False)
    supports_stream = Column(Boolean, default=True, nullable=False)
    supports_vision = Column(Boolean, default=False, nullable=False)
    supports_image_generation = Column(Boolean, default=False, nullable=False)
    supports_audio_input = Column(Boolean, default=False, nullable=False)
    supports_audio_output = Column(Boolean, default=False, nullable=False)
    supports_embeddings = Column(Boolean, default=False, nullable=False)
    supports_reasoning = Column(Boolean, default=False, nullable=False)
    supports_system_prompt = Column(Boolean, default=True, nullable=False)
    supports_web_search = Column(Boolean, default=False, nullable=False)
    supports_file_upload = Column(Boolean, default=False, nullable=False)
    supports_pdf = Column(Boolean, default=False, nullable=False)
    supports_function_call = Column(Boolean, default=False, nullable=False)
    supports_seed = Column(Boolean, default=False, nullable=False)
    supports_response_format = Column(Boolean, default=False, nullable=False)
    supports_cache = Column(Boolean, default=False, nullable=False)
    supports_citations = Column(Boolean, default=False, nullable=False)
    supports_multimodal = Column(Boolean, default=False, nullable=False)
    
    # Pricing & Performance
    typical_latency_ms = Column(Integer, default=1000, nullable=False)
    speed_tier = Column(String(50), default="standard", nullable=False)
    input_price_per_million = Column(Float, default=0.0, nullable=False)
    output_price_per_million = Column(Float, default=0.0, nullable=False)
    cache_price_per_million = Column(Float, default=0.0, nullable=False)
    priority = Column(Integer, default=0, nullable=False)
    
    # Optional / Extra
    fallback_model_id = Column(PGUUID(as_uuid=True), ForeignKey("ai_models.id"), nullable=True)
    provider_model_name = Column(String(100), nullable=True)
    api_version = Column(String(50), nullable=True)
    endpoint = Column(String(255), nullable=True)
    extra = Column(JSON, nullable=True)

    provider = relationship("AIProviderModel", back_populates="models")
    fallback_model = relationship("AIModelModel", remote_side="AIModelModel.id")
