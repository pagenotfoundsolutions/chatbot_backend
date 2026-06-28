from collections.abc import Iterator, Sequence
from typing import Any

from langchain_core.messages import AIMessage, SystemMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict

from app.modules.chat.application.ports.output.agent_port import AgentPort
from app.modules.chat.domain.entities.message import Message
from app.modules.chat.domain.exceptions.chat_exceptions import LLMProviderError
from app.modules.ai_providers.application.dto.provider_config_dto import ProviderConfigDTO
from app.modules.chat.adapters.output.llm.dynamic_llm_adapter import DynamicLLMAdapter

class AgentState(TypedDict, total=False):
    messages: Annotated[list, add_messages]

class LangGraphAgentAdapter(AgentPort):
    """Adapter for LangGraph execution.
    
    Implements AgentPort and encapsulates all LangChain/LangGraph logic.
    Does not depend on any Application Use Cases.
    """
    
    def _build_agentic_graph(self, client: Any, tools: list[Any], system_prompt: str) -> CompiledStateGraph:
        from langchain_core.runnables import RunnableConfig
        def agent_node(state: AgentState, config: RunnableConfig) -> dict[str, list[Any]]:
            llm = client.bind_tools(tools) if tools else client
            response = llm.invoke(state["messages"], config=config)
            return {"messages": [response]}

        def should_continue(state: AgentState) -> str:
            last_message = state["messages"][-1]
            if last_message.tool_calls:
                return "tools"
            return END

        workflow = StateGraph(AgentState)
        workflow.add_node("agent", agent_node)
        
        workflow.add_edge(START, "agent")
        
        if tools:
            workflow.add_node("tools", ToolNode(tools))
            workflow.add_conditional_edges("agent", should_continue)
            workflow.add_edge("tools", "agent")
        else:
            workflow.add_edge("agent", END)
            
        return workflow.compile()

    def run_graph(
        self, 
        history: Sequence[Message], 
        config: ProviderConfigDTO,
        thinking_enabled: bool,
        system_prompt: str,
        tools: list[Any]
    ) -> tuple[str, str | None]:
        try:
            client = DynamicLLMAdapter.build_client(config, thinking_enabled)
            messages = DynamicLLMAdapter.to_langchain_messages(history, system_prompt)
            graph = self._build_agentic_graph(client, tools, system_prompt)
            
            final_state = graph.invoke({
                "messages": messages
            })
            last_message = final_state["messages"][-1]
            
            content = ""
            reasoning = last_message.additional_kwargs.get("reasoning_content") if hasattr(last_message, 'additional_kwargs') else None

            # Handle structured content blocks (like Anthropic)
            if isinstance(last_message.content, list):
                text_parts = []
                for block in last_message.content:
                    if isinstance(block, dict):
                        if block.get("type") == "thinking":
                            # Anthropic stores thinking in 'thinking' key of the block
                            reasoning = block.get("thinking", "")
                        elif block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                content = "".join(text_parts).strip()
            else:
                content = str(last_message.content) if last_message.content else ""
            
            # Fallback for models that put <think> directly into content (like DeepSeek on some platforms)
            if not reasoning and "<think>" in content:
                import re
                match = re.search(r"<think>(.*?)</think>", content, flags=re.DOTALL | re.IGNORECASE)
                if match:
                    reasoning = match.group(1).strip()
                    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL | re.IGNORECASE).strip()

            if reasoning is not None:
                reasoning = str(reasoning)
            return content, reasoning
        except Exception as e:
            raise LLMProviderError(str(e))

    def stream_graph(
        self, 
        history: Sequence[Message], 
        config: ProviderConfigDTO,
        thinking_enabled: bool,
        system_prompt: str,
        tools: list[Any]
    ) -> Iterator[tuple[str, str]]:
        try:
            client = DynamicLLMAdapter.build_client(config, thinking_enabled)
            messages = DynamicLLMAdapter.to_langchain_messages(history, system_prompt)
            graph = self._build_agentic_graph(client, tools, system_prompt)
            
            input_state = {
                "messages": messages
            }
            
            # Using stream_mode="messages" yields (chunk, metadata) as they are generated by the LLM
            for chunk, metadata in graph.stream(input_state, stream_mode="messages"):
                if getattr(chunk, 'tool_call_chunks', None):
                    for tc_chunk in chunk.tool_call_chunks:
                        if tc_chunk.get("name"): # only yield when the tool name arrives
                            yield "tool_call", f"Calling tool: {tc_chunk['name']}"
                
                # We only care about AIMessageChunks for the actual text/thinking
                from langchain_core.messages import AIMessageChunk
                if isinstance(chunk, AIMessageChunk):
                    reasoning_chunk = chunk.additional_kwargs.get("reasoning_content") if hasattr(chunk, 'additional_kwargs') else None
                    
                    content_chunk = ""
                    if isinstance(chunk.content, list):
                        for block in chunk.content:
                            if isinstance(block, dict):
                                if block.get("type") == "thinking":
                                    reasoning_chunk = block.get("thinking", "")
                                elif block.get("type") == "text":
                                    content_chunk += block.get("text", "")
                            elif isinstance(block, str):
                                content_chunk += block
                    else:
                        content_chunk = str(chunk.content) if chunk.content else ""
                        
                    if reasoning_chunk:
                        yield "thinking", str(reasoning_chunk)
                    if content_chunk:
                        yield "content", str(content_chunk)
                                
        except Exception as e:
            raise LLMProviderError(str(e))
