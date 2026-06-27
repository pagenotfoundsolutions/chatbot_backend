from abc import ABC, abstractmethod
from typing import Sequence
import uuid

from langchain_core.tools import BaseTool

class ToolProviderPort(ABC):
    """Output port for fetching tools from infrastructure."""
    
    @abstractmethod
    def get_all_tools(
        self, 
        auth_user_id: uuid.UUID | None = None, 
        file_id: uuid.UUID | None = None
    ) -> Sequence[BaseTool]:
        """Returns a list of all active tools."""
        pass
