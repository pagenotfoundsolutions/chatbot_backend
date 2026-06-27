from collections.abc import Iterator, Sequence

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.modules.chat.application.ports.output.llm_port import LLMPort
from app.modules.chat.domain.entities.message import Message
from app.modules.chat.domain.exceptions.chat_exceptions import LLMProviderError
from app.modules.chat.domain.value_objects.message_role import MessageRole
from app.modules.ai_providers.application.dto.provider_config_dto import ProviderConfigDTO
from app.modules.tools.application.ports.input.get_all_tools_use_case import GetAllToolsUseCase
from langgraph.prebuilt import create_react_agent

class DynamicLLMAdapter(LLMPort):
    """Dynamic LLM implementation of the LLMPort.
    
    Instantiates the correct Langchain client based on the provider configuration
    orchestrated by the application layer.
    """

    def __init__(
        self,
        get_all_tools_use_case: GetAllToolsUseCase,
        system_prompt: str = "You are a helpful assistant.",
    ) -> None:
        self.get_all_tools_use_case = get_all_tools_use_case
        self.system_prompt = system_prompt

    def _to_langchain_messages(self, history: Sequence[Message]) -> list:
        mapping = {
            MessageRole.USER: HumanMessage,
            MessageRole.ASSISTANT: AIMessage,
            MessageRole.SYSTEM: SystemMessage,
        }
        messages = [SystemMessage(content=self.system_prompt)]
        messages.extend([mapping[m.role](content=m.content) for m in history])
        return messages

    def _get_langchain_client(self, config: ProviderConfigDTO, thinking_enabled: bool = False):
        kwargs = {}
        if config.api_key:
            kwargs["api_key"] = config.api_key
        if config.base_url:
            kwargs["base_url"] = config.base_url
            
        if thinking_enabled:
            if config.provider_name == "anthropic":
                kwargs["thinking"] = {"type": "enabled", "budget_tokens": 1024}
            elif config.provider_name == "openai":
                kwargs["reasoning_effort"] = "high"

        # Langchain provides init_chat_model to instantiate dynamically
        return init_chat_model(
            model=config.model_key,
            model_provider=config.provider_name,
            **kwargs
        )

    def generate(self, history: Sequence[Message], config: ProviderConfigDTO, thinking_enabled: bool = False) -> str:
        try:
            client = self._get_langchain_client(config, thinking_enabled)
            tools = self.get_all_tools_use_case.execute()
            messages = self._to_langchain_messages(history)
            
            if tools:
                agent = create_react_agent(client, tools=tools)
                response = agent.invoke({"messages": messages})
                return str(response["messages"][-1].content)
            else:
                response = client.invoke(messages)
                return str(response.content)
        except Exception as e:
            raise LLMProviderError(str(e))

    def stream(self, history: Sequence[Message], config: ProviderConfigDTO, thinking_enabled: bool = False) -> Iterator[tuple[str, str]]:
        try:
            client = self._get_langchain_client(config, thinking_enabled)
            tools = self.get_all_tools_use_case.execute()
            messages = self._to_langchain_messages(history)
            
            if tools:
                agent = create_react_agent(client, tools=tools)
                for msg_chunk, metadata in agent.stream({"messages": messages}, stream_mode="messages"):
                    # Yield tool execution logs
                    if isinstance(msg_chunk, AIMessage) and getattr(msg_chunk, 'tool_calls', None):
                        for tool_call in msg_chunk.tool_calls:
                            yield "tool_call", f"Calling tool: {tool_call['name']}"
                    
                    reasoning = msg_chunk.additional_kwargs.get("reasoning_content") if hasattr(msg_chunk, 'additional_kwargs') else None
                    if reasoning:
                        yield "thinking", str(reasoning)
                    
                    if getattr(msg_chunk, 'content', None) and isinstance(msg_chunk.content, str):
                        yield "content", str(msg_chunk.content)
            else:
                for chunk in client.stream(messages):
                    reasoning = chunk.additional_kwargs.get("reasoning_content")
                    if reasoning:
                        yield "thinking", str(reasoning)
                        
                    if chunk.content:
                        yield "content", str(chunk.content)
        except Exception as e:
            raise LLMProviderError(str(e))
