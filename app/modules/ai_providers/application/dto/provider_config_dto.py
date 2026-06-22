from dataclasses import dataclass

@dataclass(frozen=True)
class ProviderConfigDTO:
    """Safe DTO to transfer provider configurations across module boundaries."""
    provider_name: str
    model_key: str
    api_key: str
    base_url: str | None
