from typing import List, Dict, Any
from abc import ABC, abstractmethod

class BulkProviderItemCommand:
    def __init__(self, provider: Dict[str, Any], models: List[Dict[str, Any]]):
        self.provider = provider
        self.models = models

class BulkCreateProvidersCommand:
    def __init__(self, items: List[BulkProviderItemCommand]):
        self.items = items

class BulkCreateProvidersUseCase(ABC):
    @abstractmethod
    def execute(self, command: BulkCreateProvidersCommand) -> None:
        """
        Processes a bulk creation of providers and their models.
        """
        pass
