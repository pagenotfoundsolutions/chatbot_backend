from __future__ import annotations

from typing import TYPE_CHECKING

import uuid
from sqlalchemy import String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

from app.shared.database.database import Base
from app.shared.database.core_model import CoreModelMixin

if TYPE_CHECKING:
    from app.modules.chat.adapters.output.persistence.models.conversation_model import (
        ConversationModel,
    )


class MessageModel(CoreModelMixin, Base):
    """ORM row for a single turn in a conversation."""

    __tablename__ = "messages"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    conversation: Mapped["ConversationModel"] = relationship(back_populates="messages")
