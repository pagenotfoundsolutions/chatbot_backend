from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Annotated, TypedDict

from app.modules.chat.infrastructure.config.chat_config import ChatConfig

if TYPE_CHECKING:
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.messages import BaseMessage


class ChatState(TypedDict):
    """LangGraph state: the running list of messages.

    `add_messages` is a reducer — node return values are appended to the list
    rather than replacing it, which is what lets later phases add retrieval /
    tool nodes that each contribute messages.
    """

    # `Annotated[..., add_messages]` is resolved lazily in build_chat_graph to
    # avoid importing langgraph at module load time.
    messages: list


def build_chat_graph(model: "BaseChatModel", config: ChatConfig):
    """Compile a minimal LangGraph chat graph around a chat model.

    Today it's a single `model` node: prepend the system prompt, call the LLM,
    append the reply. The graph shape is deliberate — Phase 2 (RAG) and beyond
    slot retrieval/tool nodes in front of this node without changing the seam.
    """
    from langgraph.graph import START, StateGraph
    from langgraph.graph.message import add_messages

    class _State(TypedDict):
        messages: Annotated[list, add_messages]

    def call_model(state: _State) -> dict:
        from langchain_core.messages import SystemMessage

        history: list[BaseMessage] = [
            SystemMessage(content=config.system_prompt),
            *state["messages"],
        ]
        reply = model.invoke(history)
        return {"messages": [reply]}

    graph = StateGraph(_State)
    graph.add_node("model", call_model)
    graph.add_edge(START, "model")
    return graph.compile()


def stream_graph(graph, messages: list["BaseMessage"]) -> Iterator[str]:
    """Stream the assistant reply token-by-token from a compiled graph.

    Uses LangGraph's `messages` stream mode, which surfaces the underlying chat
    model's token chunks as they are produced.
    """
    for chunk, _meta in graph.stream(
        {"messages": messages}, stream_mode="messages"
    ):
        text = getattr(chunk, "content", "")
        if text:
            yield text
