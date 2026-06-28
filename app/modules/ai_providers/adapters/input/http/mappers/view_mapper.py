from app.modules.ai_providers.domain.entities.ai_provider import AIProvider
from app.modules.ai_providers.domain.entities.ai_model import AIModel
from app.modules.ai_providers.adapters.input.http.api.schemas import AIProviderResponse, AIModelResponse

class AIProvidersViewMapper:
    @staticmethod
    def provider(provider: AIProvider) -> AIProviderResponse:
        return AIProviderResponse(
            id=provider.id,
            name=provider.name,
            display_name=provider.display_name,
            description=provider.description,
            api_base_url=provider.api_base_url,
            created_at=provider.created_at,
            updated_at=provider.updated_at,
            models=[AIProvidersViewMapper.model(m) for m in provider.ai_models]
        )

    @staticmethod
    def model(model: AIModel) -> AIModelResponse:
        return AIModelResponse(
            id=model.id,
            provider_id=model.provider_id,
            model_key=model.model_key,
            display_name=model.display_name,
            description=model.description,
            is_active=model.is_active,
            is_default=model.is_default,
            is_deprecated=model.is_deprecated,
            model_type=model.model_type,
            max_input_tokens=model.max_input_tokens,
            max_output_tokens=model.max_output_tokens,
            max_context_window=model.max_context_window,
            default_temperature=model.default_temperature,
            default_top_p=model.default_top_p,
            default_frequency_penalty=model.default_frequency_penalty,
            default_presence_penalty=model.default_presence_penalty,
            capabilities=model.capabilities,
            typical_latency_ms=model.typical_latency_ms,
            speed_tier=model.speed_tier,
            input_price_per_million=model.input_price_per_million,
            output_price_per_million=model.output_price_per_million,
            cache_price_per_million=model.cache_price_per_million,
            priority=model.priority,
            fallback_model_id=model.fallback_model_id,
            provider_model_name=model.provider_model_name,
            api_version=model.api_version,
            endpoint=model.endpoint,
            extra=model.extra,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
