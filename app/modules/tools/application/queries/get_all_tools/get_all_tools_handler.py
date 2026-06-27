from typing import Sequence

from langchain_core.tools import BaseTool

from app.modules.tools.adapters.output.tool_registry import ToolRegistry
from app.modules.tools.application.ports.input.get_all_tools_use_case import GetAllToolsUseCase


class GetAllToolsHandler(GetAllToolsUseCase):
    """Executes the query to fetch all available tools."""

    def execute(self) -> Sequence[BaseTool]:
        # For Phase 1, we just return the native and manual tools from the registry
        return ToolRegistry.get_all_tools()
