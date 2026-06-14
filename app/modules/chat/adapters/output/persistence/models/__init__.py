"""ORM models for the chat module.

Importing this package registers the chat tables on `Base.metadata` so that
`init_db()` can create them. `init_db` imports this package for that side effect.
"""

from app.modules.chat.adapters.output.persistence.models.conversation_model import (
    ConversationModel,
)
from app.modules.chat.adapters.output.persistence.models.message_model import (
    MessageModel,
)

__all__ = ["ConversationModel", "MessageModel"]
