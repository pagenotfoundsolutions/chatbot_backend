import uuid
from datetime import datetime
from typing import Optional

from app.shared.kernel.aggregate_root import AggregateRoot
from app.shared.kernel.utils import generate_uuid, utc_now
from app.modules.ai_providers.domain.entities.ai_model import AIModel

class AIProvider(AggregateRoot[uuid.UUID]):
    """A single provider of AI models (e.g., OpenAI, Anthropic, Gemini).
    
    This is an Aggregate Root. It manages its own state and its collection of AIModels.
    Identity is `id` (handled by the Entity base).
    """

    def __init__(
        self,
        id: uuid.UUID,
        name: str,
        display_name: str,
        description: str,
        api_base_url: str,
        api_key: str,
        created_at: datetime,
        updated_at: datetime,
        ai_models: Optional[list[AIModel]] = None
    ) -> None:
        """
        __init__ is strictly used to REBUILD the object (e.g., when loading from Database).
        That is why it requires `id`, `created_at`, and `updated_at` to be passed in.
        """
        super().__init__(id)
        
        if not name or not name.strip():
            raise ValueError("Provider name cannot be empty")
            
        self._name = name.strip()
        self._display_name = display_name
        self._description = description
        self._api_base_url = api_base_url
        self._api_key = api_key
        self._created_at = created_at
        self._updated_at = updated_at
        self._ai_models = ai_models if ai_models is not None else []

    @classmethod
    def create(
        cls, 
        name: str, 
        display_name: str, 
        description: str, 
        api_base_url: str, 
        api_key: str
    ) -> "AIProvider":
        """
        `create` is a factory method used when making a BRAND NEW provider for the very first time.
        It generates a fresh UUID and current timestamps.
        """
        now = utc_now()
        
        # We can just use generate_uuid() directly now
        new_id = generate_uuid()
        
        return cls(
            id=new_id, 
            name=name,
            display_name=display_name,
            description=description,
            api_base_url=api_base_url,
            api_key=api_key,
            created_at=now,
            updated_at=now
        )

    # --- Aggregate Root Behaviors ---

    def update_api_key(self, new_api_key: str) -> None:
        self._api_key = new_api_key
        self._touch()

    # --- Internals ---
    
    def _touch(self) -> None:
        """Update the last modified timestamp. Call this whenever internal state changes."""
        self._updated_at = utc_now()

    # --- Properties (Getters) ---

    @property
    def name(self) -> str:
        return self._name

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def description(self) -> str:
        return self._description

    @property
    def api_base_url(self) -> str:
        return self._api_base_url

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    @property
    def ai_models(self) -> list[AIModel]:
        return self._ai_models

    