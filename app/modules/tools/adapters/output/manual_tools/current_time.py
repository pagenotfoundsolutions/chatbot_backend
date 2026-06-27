from datetime import datetime
from langchain_core.tools import tool
from pydantic import BaseModel

class CurrentTimeInput(BaseModel):
    pass

@tool(args_schema=CurrentTimeInput)
def get_current_time() -> str:
    """Returns the current date and time of the server. Use this when the user asks for the current time or date."""
    return f"The current date and time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
