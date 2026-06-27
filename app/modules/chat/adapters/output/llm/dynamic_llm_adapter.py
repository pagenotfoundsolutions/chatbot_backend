from collections.abc import Iterator, Sequence

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.modules.chat.application.ports.output.llm_port import LLMPort
from app.modules.chat.domain.entities.message import Message
from app.modules.chat.domain.exceptions.chat_exceptions import LLMProviderError
from app.modules.chat.domain.value_objects.message_role import MessageRole
from app.modules.ai_providers.application.dto.provider_config_dto import ProviderConfigDTO


class DynamicLLMAdapter(LLMPort):
    """Dynamic LLM implementation of the LLMPort.
    
    Instantiates the correct Langchain client based on the provider configuration.
    """

    def __init__(
        self,
        system_prompt: str = "You are a helpful assistant.",
    ) -> None:
        self.system_prompt = system_prompt

    @staticmethod
    def to_langchain_messages(history: Sequence[Message], system_prompt: str) -> list:
        mapping = {
            MessageRole.USER: HumanMessage,
            MessageRole.ASSISTANT: AIMessage,
            MessageRole.SYSTEM: SystemMessage,
        }
        messages = [SystemMessage(content=system_prompt)]
        messages.extend([mapping[m.role](content=m.content) for m in history])
        return messages

    @staticmethod
    def build_client(config: ProviderConfigDTO, thinking_enabled: bool = False): 
        kwargs = {
            "temperature": config.temperature,
            "timeout": 1200.0, # Increased timeout for reasoning models
            "model_kwargs": {
                "top_p": config.top_p,
                "frequency_penalty": config.frequency_penalty,
                "presence_penalty": config.presence_penalty,
            }
        }
        
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

    def generate(self, history: Sequence[Message], config: ProviderConfigDTO, thinking_enabled: bool = False, context: dict | None = None) -> str:
        try:
            client = self.build_client(config, thinking_enabled)
            messages = self.to_langchain_messages(history, self.system_prompt)
            response = client.invoke(messages)
            return str(response.content)
        except Exception as e:
            raise LLMProviderError(str(e))

    def stream(self, history: Sequence[Message], config: ProviderConfigDTO, thinking_enabled: bool = False, context: dict | None = None) -> Iterator[tuple[str, str]]:
        try:
            client = self.build_client(config, thinking_enabled)
            messages = self.to_langchain_messages(history, self.system_prompt)
            for chunk in client.stream(messages):
                reasoning = chunk.additional_kwargs.get("reasoning_content")
                if reasoning:
                    yield "thinking", str(reasoning)
                if chunk.content:
                    yield "content", str(chunk.content)
        except Exception as e:
            raise LLMProviderError(str(e))
