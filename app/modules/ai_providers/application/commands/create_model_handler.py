import uuid

from app.modules.ai_providers.domain.entities.ai_model import AIModel
from app.modules.ai_providers.application.ports.output.model_repository_port import ModelRepositoryPort
from app.modules.ai_providers.application.ports.input.create_model_use_case import CreateModelUseCase, CreateModelCommand

class CreateModelHandler(CreateModelUseCase):
    def __init__(self, model_repo: ModelRepositoryPort):
        self._model_repo = model_repo

    def execute(self, command: CreateModelCommand) -> AIModel:
        model = AIModel(
            id=uuid.uuid4(),
            provider_id=command.provider_id,
            model_key=command.model_key,
            display_name=command.display_name,
            description=command.description or "",
            is_active=command.is_active,
            is_default=command.is_default,
            is_deprecated=command.is_deprecated,
            model_type=command.model_type,
            max_input_tokens=command.max_input_tokens,
            max_output_tokens=command.max_output_tokens,
            max_context_window=command.max_context_window,
            default_temperature=command.default_temperature,
            default_top_p=command.default_top_p,
            default_frequency_penalty=command.default_frequency_penalty,
            default_presence_penalty=command.default_presence_penalty,
            supports_tools=command.supports_tools,
            supports_parallel_tools=command.supports_parallel_tools,
            supports_structured_output=command.supports_structured_output,
            supports_json=command.supports_json,
            supports_stream=command.supports_stream,
            supports_vision=command.supports_vision,
            supports_image_generation=command.supports_image_generation,
            supports_audio_input=command.supports_audio_input,
            supports_audio_output=command.supports_audio_output,
            supports_embeddings=command.supports_embeddings,
            supports_reasoning=command.supports_reasoning,
            supports_system_prompt=command.supports_system_prompt,
            supports_web_search=command.supports_web_search,
            supports_file_upload=command.supports_file_upload,
            supports_pdf=command.supports_pdf,
            supports_function_call=command.supports_function_call,
            supports_seed=command.supports_seed,
            supports_response_format=command.supports_response_format,
            supports_cache=command.supports_cache,
            supports_citations=command.supports_citations,
            supports_multimodal=command.supports_multimodal,
            typical_latency_ms=command.typical_latency_ms,
            speed_tier=command.speed_tier,
            input_price_per_million=command.input_price_per_million,
            output_price_per_million=command.output_price_per_million,
            cache_price_per_million=command.cache_price_per_million,
            priority=command.priority,
            fallback_model_id=command.fallback_model_id,
            provider_model_name=command.provider_model_name,
            api_version=command.api_version,
            endpoint=command.endpoint,
            extra=command.extra
        )
        
        self._model_repo.save(model)
        return model
