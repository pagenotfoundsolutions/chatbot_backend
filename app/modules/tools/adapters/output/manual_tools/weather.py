import json
import urllib.request
from urllib.parse import quote
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str = Field(description="The name of the city or location to get the weather for (e.g., 'Delhi')")

class WeatherOutput(BaseModel):
    location: str
    temperature_c: str | None = None
    description: str | None = None
    humidity: str | None = None
    wind_kmh: str | None = None
    error: str | None = None

@tool(args_schema=WeatherInput)
def get_weather(location: str) -> str:
    """Gets the current weather for a specific location and returns it in a structured JSON format."""
    try:
        url = f"https://wttr.in/{quote(location)}?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            current = data['current_condition'][0]
            output = WeatherOutput(
                location=location,
                temperature_c=current['temp_C'],
                description=current['weatherDesc'][0]['value'],
                humidity=current['humidity'],
                wind_kmh=current['windspeedKmph']
            )
            return output.model_dump_json()
    except Exception as e:
        return WeatherOutput(location=location, error=str(e)).model_dump_json()
