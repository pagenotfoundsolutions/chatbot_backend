from __future__ import annotations

from functools import lru_cache

from app.modules.chat.infrastructure.config.chat_config import ChatConfig, get_chat_config
from app.shared.config.settings import Settings, get_settings


class DependencyContainer:
    """Application-wide composition root for process-level singletons.

    Per-request wiring (repositories bound to a request-scoped DB session) stays
    in each module's `adapters/input/http/dependencies.py` via FastAPI `Depends`.
    This container holds only things that live for the whole process — config and
    other stateless singletons — and gives them one discoverable home.
    """

    @property
    def settings(self) -> Settings:
        return get_settings()

    @property
    def chat_config(self) -> ChatConfig:
        return get_chat_config()


@lru_cache
def get_container() -> DependencyContainer:
    return DependencyContainer()
