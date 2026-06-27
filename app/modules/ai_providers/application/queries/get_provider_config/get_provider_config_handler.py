import uuid

from app.modules.ai_providers.application.ports.input.get_provider_config_use_case import GetProviderConfigUseCase
from app.modules.ai_providers.application.dto.provider_config_dto import ProviderConfigDTO
from app.modules.ai_providers.application.ports.output.provider_repository_port import ProviderRepositoryPort
from app.modules.ai_providers.application.ports.output.model_repository_port import ModelRepositoryPort

class GetProviderConfigHandler(GetProviderConfigUseCase):
    """Handles fetching and assembling the ProviderConfigDTO."""
    
    def __init__(
        self, 
        provider_repo: ProviderRepositoryPort, 
        model_repo: ModelRepositoryPort
    ) -> None:
        self._provider_repo = provider_repo
        self._model_repo = model_repo

    def execute(self, provider_id: uuid.UUID, model_id: uuid.UUID) -> ProviderConfigDTO | None:
        provider = self._provider_repo.get(provider_id)
        if not provider:
            return None
            
        model = self._model_repo.get(model_id)
        if not model or not model.is_active:
            return None
            
        if model.provider_id != provider.id:
            return None

        return ProviderConfigDTO(
            provider_name=provider.name.lower(),
            model_key=model.model_key,
            api_key=provider.api_key,
            base_url=provider.api_base_url if provider.api_base_url else None,
            temperature=model.default_temperature,
            top_p=model.default_top_p,
            frequency_penalty=model.default_frequency_penalty,
            presence_penalty=model.default_presence_penalty,
            supports_reasoning=model.supports_reasoning,
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
            supports_system_prompt=model.supports_system_prompt,
            supports_web_search=model.supports_web_search,
            supports_file_upload=model.supports_file_upload,
            supports_pdf=model.supports_pdf,
            supports_function_call=model.supports_function_call,
            supports_seed=model.supports_seed,
            supports_response_format=model.supports_response_format,
            supports_cache=model.supports_cache,
            supports_citations=model.supports_citations
        )
