from dataclasses import dataclass

@dataclass(frozen=True)
class ProviderConfigDTO:
    """Safe DTO to transfer provider configurations across module boundaries."""
    provider_name: str
    model_key: str
    api_key: str
    base_url: str | None
    
    # Model Hyperparameters
    temperature: float
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    
    # Capabilities
    supports_reasoning: bool
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
    supports_system_prompt: bool
    supports_web_search: bool
    supports_file_upload: bool
    supports_pdf: bool
    supports_function_call: bool
    supports_seed: bool
    supports_response_format: bool
    supports_cache: bool
    supports_citations: bool
