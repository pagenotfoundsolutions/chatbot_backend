from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import TYPE_CHECKING

from app.modules.chat.adapters.output.llm.chat_graph import (
    build_chat_graph,
    stream_graph,
)
from app.modules.chat.adapters.output.llm.model_factory import build_chat_model
from app.modules.chat.application.ports.output.llm_port import LLMPort
from app.modules.chat.domain.entities.message import Message
from app.modules.chat.domain.value_objects.message_role import MessageRole
from app.modules.chat.infrastructure.config.chat_config import ChatConfig

if TYPE_CHECKING:
    from langchain_core.messages import BaseMessage


class LangChainLLMAdapter(LLMPort):
    """Driven adapter implementing `LLMPort` via LangChain + LangGraph.

    Provider-agnostic: the concrete chat model (OpenAI / Anthropic / Ollama /
    HuggingFace) is chosen by `ChatConfig` and built by the model factory; the
    conversation flow runs through a compiled LangGraph graph. The domain stays
    unaware of all of it.
    """

    def __init__(self, config: ChatConfig) -> None:
        self._config = config
        model = build_chat_model(config)
        self._graph = build_chat_graph(model, config)

    def generate(self, history: Sequence[Message]) -> str:
        messages = self._to_langchain(history)
        result = self._graph.invoke({"messages": messages})
        final = result["messages"][-1]
        return getattr(final, "content", "") or ""

    def stream(self, history: Sequence[Message]) -> Iterator[str]:
        messages = self._to_langchain(history)
        yield from stream_graph(self._graph, messages)

    # --- mapping -----------------------------------------------------------
    @staticmethod
    def _to_langchain(history: Sequence[Message]) -> list["BaseMessage"]:
        from langchain_core.messages import (
            AIMessage,
            HumanMessage,
            SystemMessage,
        )

        mapping = {
            MessageRole.USER: HumanMessage,
            MessageRole.ASSISTANT: AIMessage,
            MessageRole.SYSTEM: SystemMessage,
        }
        return [mapping[m.role](content=m.content) for m in history]
