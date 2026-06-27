from typing import Sequence
import uuid

from langchain_core.tools import BaseTool

from app.modules.tools.application.ports.output.tool_provider_port import ToolProviderPort
from app.modules.tools.application.ports.input.get_all_tools_use_case import GetAllToolsUseCase

class GetAllToolsHandler(GetAllToolsUseCase):
    """Executes the query to fetch all available tools."""

    def __init__(self, tool_provider: ToolProviderPort) -> None:
        self._tool_provider = tool_provider

    def execute(
        self, 
        auth_user_id: uuid.UUID | None = None, 
        file_id: uuid.UUID | None = None
    ) -> Sequence[BaseTool]:
        # For Phase 1, we just return the native and manual tools from the registry
        return self._tool_provider.get_all_tools(auth_user_id, file_id)
