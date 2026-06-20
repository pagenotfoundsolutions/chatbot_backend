from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

from app.modules.chat.adapters.output.persistence.models.message_model import (
    MessageModel,
)
from app.shared.database.database import Base
from app.shared.database.core_model import CoreModelMixin


class ConversationModel(CoreModelMixin, Base):
    """ORM row for a conversation. Pure persistence concern — kept separate from
    the domain `Conversation` aggregate and bridged by a mapper."""

    __tablename__ = "conversations"

    auth_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("auth_users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    messages: Mapped[list[MessageModel]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="MessageModel.created_at",
        lazy="selectin",
    )
