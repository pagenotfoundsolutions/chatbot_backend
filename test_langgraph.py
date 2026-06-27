import asyncio
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

@tool
def get_time():
    """get current time"""
    return "12:00"

async def main():
    try:
        client = ChatOpenAI(model="gpt-3.5-turbo", api_key="sk-test", base_url="http://localhost:8000")
    except Exception as e:
        print("client error", e)
        return
    agent = create_react_agent(client, tools=[get_time])
    try:
        # Note: since api_key is fake, it will fail but we want to see if it even reaches the loop.
        for event in agent.stream({"messages": [("user", "hi")]}, stream_mode="messages"):
            print(event)
    except Exception as e:
        print("stream error:", e)

asyncio.run(main())
