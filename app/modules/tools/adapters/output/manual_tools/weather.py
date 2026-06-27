import json
import urllib.request
from urllib.parse import quote
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str = Field(description="The name of the city or location to get the weather for (e.g., 'Delhi')")

@tool(args_schema=WeatherInput)
def get_weather(location: str) -> str:
    """Gets the current weather for a specific location. Use this when the user asks about the weather."""
    try:
        url = f"https://wttr.in/{quote(location)}?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            current = data['current_condition'][0]
            temp_c = current['temp_C']
            desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            wind = current['windspeedKmph']
            return f"Weather in {location}: {desc}, Temperature: {temp_c}°C, Humidity: {humidity}%, Wind: {wind} km/h"
    except Exception as e:
        return f"Could not fetch weather for {location}: {str(e)}"
