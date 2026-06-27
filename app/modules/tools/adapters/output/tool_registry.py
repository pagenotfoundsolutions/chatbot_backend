from datetime import datetime
from typing import Sequence

from langchain_core.tools import BaseTool, tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


import numexpr

@tool
def get_current_time() -> str:
    """Returns the current date and time. Use this when the user asks for the time or date."""
    return f"The current date and time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."

@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression (e.g., '12 * (3 + 4)'). Use this for math, arithmetic, or calculations."""
    try:
        # numexpr safely evaluates math expressions without the risk of arbitrary code execution
        result = numexpr.evaluate(expression)
        return str(result.item() if hasattr(result, "item") else result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

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
            calculator
        ]
