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
            supports_tools=model.supports_tools,
            supports_parallel_tools=model.supports_parallel_tools,
            supports_structured_output=model.supports_structured_output,
            supports_json=model.supports_json,
            supports_stream=model.supports_stream,
            supports_vision=model.supports_vision,
            supports_image_generation=model.supports_image_generation,
            supports_audio_input=model.supports_audio_input,
            supports_audio_output=model.supports_audio_output,
            supports_embeddings=model.supports_embeddings,
            supports_reasoning=model.supports_reasoning,
            supports_system_prompt=model.supports_system_prompt,
            supports_web_search=model.supports_web_search,
            supports_file_upload=model.supports_file_upload,
            supports_pdf=model.supports_pdf,
            supports_function_call=model.supports_function_call,
            supports_seed=model.supports_seed,
            supports_response_format=model.supports_response_format,
            supports_cache=model.supports_cache,
            supports_citations=model.supports_citations,
            supports_multimodal=model.supports_multimodal,
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
