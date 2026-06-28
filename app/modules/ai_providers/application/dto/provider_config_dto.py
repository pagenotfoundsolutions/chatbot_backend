from dataclasses import dataclass
from app.modules.ai_providers.domain.value_objects.model_capability import ModelCapability

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
    capabilities: list[ModelCapability]
    
    def supports(self, capability: ModelCapability | str) -> bool:
        """Check if a specific capability is supported."""
        if isinstance(capability, str):
            try:
                capability = ModelCapability(capability)
            except ValueError:
                return False
        return capability in self.capabilities
