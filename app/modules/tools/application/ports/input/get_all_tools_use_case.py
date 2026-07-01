from abc import ABC, abstractmethod
from typing import Sequence
import uuid

from langchain_core.tools import BaseTool

class GetAllToolsUseCase(ABC):
    """Driving port: Fetches all available tools (Native, Manual, and MCP)."""

    @abstractmethod
    def execute(
        self, 
        auth_user_id: uuid.UUID | None = None, 
        file_ids: set[uuid.UUID] | list[uuid.UUID] | None = None
    ) -> Sequence[BaseTool]:
        """Returns the active list of tools."""
        pass
