from abc import ABC, abstractmethod
from typing import Sequence

from langchain_core.tools import BaseTool


class GetAllToolsUseCase(ABC):
    """Driving port: Fetches all available tools (Native, Manual, and MCP)."""

    @abstractmethod
    def execute(self) -> Sequence[BaseTool]:
        """Returns the active list of LangChain tools."""
        pass
