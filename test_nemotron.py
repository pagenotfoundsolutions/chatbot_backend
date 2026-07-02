import os
import sys
from app.shared.config.settings import settings
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.tools import tool

@tool
def dummy_tool(x: str) -> str:
    """A dummy tool."""
    return x

llm = ChatNVIDIA(model="nvidia/nemotron-3-ultra-550b-a55b", api_key=settings.ai_providers.get("nvidia_nim", ""))
llm_with_tools = llm.bind_tools([dummy_tool])

try:
    resp = llm_with_tools.invoke("Use the dummy tool with value 'hello'")
    print("SUCCESS")
    print(resp)
except Exception as e:
    print(f"FAILED: {e}")
