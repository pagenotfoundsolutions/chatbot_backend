from abc import ABC, abstractmethod
from typing import Any, Dict
from uuid import UUID

class TokenGeneratorPort(ABC):
    @abstractmethod
    def generate_access_token(self, user_id: UUID) -> str:
        """Generate a short-lived access token."""
        pass

    @abstractmethod
    def generate_refresh_token(self, user_id: UUID) -> str:
        """Generate a long-lived opaque refresh token."""
        pass

    @abstractmethod
    def verify_access_token(self, token: str) -> Dict[str, Any]:
        """Verify the access token and return its payload."""
        pass
