from datetime import datetime
from typing import Sequence

from langchain_core.tools import BaseTool, tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from .manual_tools.calculator import calculator
from .manual_tools.weather import get_weather
from .manual_tools.current_time import get_current_time

class ToolRegistry:
    """Registry that instantiates and holds all active native and manual tools."""

    @classmethod
    def get_all_tools(cls) -> Sequence[BaseTool]:
        """Returns a list of all initialized LangChain tools."""
        
        # Initialize native tools
        search_tool = DuckDuckGoSearchRun()
        wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        
        # Combine native and manual tools
        return [
            search_tool,
            wikipedia_tool,
            get_current_time,
            calculator,
            get_weather
        ]
