from app.modules.tools.application.queries.get_all_tools.get_all_tools_handler import GetAllToolsHandler
from app.modules.tools.application.ports.input.get_all_tools_use_case import GetAllToolsUseCase
from app.modules.tools.application.ports.output.tool_provider_port import ToolProviderPort
from app.modules.rag.application.ports.input.search_chunks_use_case import SearchChunksUseCase
from app.modules.rag.adapters.input.http.dependencies import get_search_chunks_use_case
from fastapi import Depends

def get_tool_provider(
    search_chunks_use_case: SearchChunksUseCase = Depends(get_search_chunks_use_case)
) -> ToolProviderPort:
    from app.modules.tools.adapters.output.tool_registry import LangchainToolProviderAdapter
    return LangchainToolProviderAdapter(search_chunks_use_case=search_chunks_use_case)

def get_all_tools_use_case(tool_provider: ToolProviderPort = Depends(get_tool_provider)) -> GetAllToolsUseCase:
    """Dependency provider for GetAllToolsUseCase."""
    return GetAllToolsHandler(tool_provider=tool_provider)
