import warnings
from collections.abc import Iterator, Sequence

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# Suppress the harmless unknown model warning from langchain-nvidia
warnings.filterwarnings(
    "ignore",
    message="Found .* in available_models, but type is unknown",
    category=UserWarning,
)

from app.modules.chat.application.ports.output.llm_port import LLMPort
from app.modules.chat.domain.entities.message import Message
from app.modules.chat.domain.value_objects.message_role import MessageRole
from app.modules.chat.infrastructure.config.chat_config import ChatConfig


class NvidiaLLMAdapter(LLMPort):
    """Direct NVIDIA LLM implementation of the LLMPort.
    
    Bypasses complex generic model factories and LangGraph to directly
    fulfill the port contract using the NVIDIA endpoints.
    """

    def __init__(self, config: ChatConfig) -> None:
        self.model = ChatNVIDIA(
            model=config.model or "nvidia/nemotron-3-ultra-550b-a55b",
            api_key=config.nvidia_api_key,
            temperature=config.temperature,
            top_p=config.top_p,
            max_tokens=config.max_tokens,
            model_kwargs={
                "reasoning_budget": config.reasoning_budget,
            },
        )
            # "chat_template_kwargs": {"enable_thinking": True},
        self.system_prompt = config.system_prompt

    def _to_langchain_messages(self, history: Sequence[Message]) -> list:
        mapping = {
            MessageRole.USER: HumanMessage,
            MessageRole.ASSISTANT: AIMessage,
            MessageRole.SYSTEM: SystemMessage,
        }
        
        messages = []
        if self.system_prompt:
            messages.append(SystemMessage(content=self.system_prompt))
            
        messages.extend([mapping[m.role](content=m.content) for m in history])
        return messages

    def generate(self, history: Sequence[Message]) -> str:
        messages = self._to_langchain_messages(history)
        response = self.model.invoke(messages)
        return str(response.content)

    def stream(self, history: Sequence[Message]) -> Iterator[str]:
        messages = self._to_langchain_messages(history)
        for chunk in self.model.stream(messages):
            if chunk.content:
                yield str(chunk.content)
