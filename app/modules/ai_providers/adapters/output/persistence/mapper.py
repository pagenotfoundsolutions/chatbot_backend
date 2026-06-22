from typing import Optional
from app.modules.ai_providers.domain.entities.ai_provider import AIProvider
from app.modules.ai_providers.domain.entities.ai_model import AIModel
from app.modules.ai_providers.adapters.output.persistence.models.ai_provider_model import AIProviderModel
from app.modules.ai_providers.adapters.output.persistence.models.ai_model_model import AIModelModel

class ProviderMapper:
    @staticmethod
    def to_domain(model: AIProviderModel) -> AIProvider:
        if not model:
            return None
        return AIProvider(
            id=model.id,
            name=model.name,
            display_name=model.display_name,
            description=model.description,
            api_base_url=model.api_base_url,
            api_key=model.api_key,
            created_at=model.created_at,
            updated_at=model.updated_at,
            ai_models=[ModelMapper.to_domain(ai_model) for ai_model in model.models]
        )

    @staticmethod
    def to_model(entity: AIProvider) -> AIProviderModel:
        if not entity:
            return None
        return AIProviderModel(
            id=entity.id,
            name=entity.name,
            display_name=entity.display_name,
            description=entity.description,
            api_base_url=entity.api_base_url,
            api_key=entity.api_key,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

class ModelMapper:
    @staticmethod
    def to_domain(model: AIModelModel) -> AIModel:
        if not model:
            return None
        return AIModel(
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
            updated_at=model.updated_at,
            deleted_at=model.deleted_at
        )

    @staticmethod
    def to_model(entity: AIModel) -> AIModelModel:
        if not entity:
            return None
        return AIModelModel(
            id=entity.id,
            provider_id=entity.provider_id,
            model_key=entity.model_key,
            display_name=entity.display_name,
            description=entity.description,
            is_active=entity.is_active,
            is_default=entity.is_default,
            is_deprecated=entity.is_deprecated,
            model_type=entity.model_type,
            max_input_tokens=entity.max_input_tokens,
            max_output_tokens=entity.max_output_tokens,
            max_context_window=entity.max_context_window,
            default_temperature=entity.default_temperature,
            default_top_p=entity.default_top_p,
            default_frequency_penalty=entity.default_frequency_penalty,
            default_presence_penalty=entity.default_presence_penalty,
            supports_tools=entity.supports_tools,
            supports_parallel_tools=entity.supports_parallel_tools,
            supports_structured_output=entity.supports_structured_output,
            supports_json=entity.supports_json,
            supports_stream=entity.supports_stream,
            supports_vision=entity.supports_vision,
            supports_image_generation=entity.supports_image_generation,
            supports_audio_input=entity.supports_audio_input,
            supports_audio_output=entity.supports_audio_output,
            supports_embeddings=entity.supports_embeddings,
            supports_reasoning=entity.supports_reasoning,
            supports_system_prompt=entity.supports_system_prompt,
            supports_web_search=entity.supports_web_search,
            supports_file_upload=entity.supports_file_upload,
            supports_pdf=entity.supports_pdf,
            supports_function_call=entity.supports_function_call,
            supports_seed=entity.supports_seed,
            supports_response_format=entity.supports_response_format,
            supports_cache=entity.supports_cache,
            supports_citations=entity.supports_citations,
            supports_multimodal=entity.supports_multimodal,
            typical_latency_ms=entity.typical_latency_ms,
            speed_tier=entity.speed_tier,
            input_price_per_million=entity.input_price_per_million,
            output_price_per_million=entity.output_price_per_million,
            cache_price_per_million=entity.cache_price_per_million,
            priority=entity.priority,
            fallback_model_id=entity.fallback_model_id,
            provider_model_name=entity.provider_model_name,
            api_version=entity.api_version,
            endpoint=entity.endpoint,
            extra=entity.extra,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at
        )
