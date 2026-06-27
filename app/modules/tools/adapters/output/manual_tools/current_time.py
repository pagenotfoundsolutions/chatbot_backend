from datetime import datetime
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class CurrentTimeInput(BaseModel):
    pass

class CurrentTimeOutput(BaseModel):
    datetime: str = Field(description="The ISO format datetime")
    formatted: str = Field(description="The human readable datetime")

@tool(args_schema=CurrentTimeInput)
def get_current_time() -> str:
    """Returns the current date and time of the server in a structured JSON format."""
    now = datetime.now()
    output = CurrentTimeOutput(
        datetime=now.isoformat(),
        formatted=now.strftime('%Y-%m-%d %H:%M:%S')
    )
    return output.model_dump_json()
