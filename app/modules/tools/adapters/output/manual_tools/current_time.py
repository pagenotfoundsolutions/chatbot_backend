from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class CurrentTimeInput(BaseModel):
    timezone: str = Field(
        default="UTC", 
        description="The timezone to get the current time for, e.g. 'Asia/Kolkata', 'America/New_York', 'UTC'"
    )

class CurrentTimeOutput(BaseModel):
    datetime: str = Field(description="The ISO format datetime")
    formatted: str = Field(description="The human readable datetime")
    timezone: str = Field(description="The timezone used")

@tool(args_schema=CurrentTimeInput)
def get_current_time(timezone: str = "UTC") -> str:
    """Returns the current date and time for a given timezone in a structured JSON format."""
    try:
        tz = ZoneInfo(timezone)
        resolved_tz = timezone
    except (ZoneInfoNotFoundError, ValueError):
        tz = ZoneInfo("UTC")
        resolved_tz = "UTC (fallback due to invalid timezone)"
        
    now = datetime.now(tz)
    output = CurrentTimeOutput(
        datetime=now.isoformat(),
        formatted=now.strftime('%Y-%m-%d %H:%M:%S %Z'),
        timezone=resolved_tz
    )
    return output.model_dump_json()
