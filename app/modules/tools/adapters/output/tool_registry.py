from typing import Sequence
import uuid

from langchain_core.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from app.modules.tools.application.ports.output.tool_provider_port import ToolProviderPort
from app.modules.rag.application.ports.input.search_chunks_use_case import SearchChunksUseCase
from .manual_tools.calculator import calculator
from .manual_tools.weather import get_weather
from .manual_tools.current_time import get_current_time
from .manual_tools.rag_search import build_rag_tool

class LangchainToolProviderAdapter(ToolProviderPort):
    """Adapter that instantiates and returns all active native and manual tools."""

    def __init__(self, search_chunks_use_case: SearchChunksUseCase | None = None):
        self._search_chunks = search_chunks_use_case

    def get_all_tools(
        self, 
        auth_user_id: uuid.UUID | None = None, 
        file_id: uuid.UUID | None = None
    ) -> Sequence[BaseTool]:
        """Returns a list of all initialized LangChain tools."""
        
        # Initialize native tools
        search_tool = DuckDuckGoSearchRun()
        wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        
        # Combine native and manual tools
        tools = [
            search_tool,
            wikipedia_tool,
            get_current_time,
            calculator,
            get_weather,
        ]
        
        # Only add the document search tool if there is a file context available
        if file_id is not None:
            tools.append(build_rag_tool(auth_user_id, file_id, self._search_chunks))
            
        return tools
