from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.modules.chat.adapters.output.persistence.models.message_model import (
    MessageModel,
)
from app.shared.database.database import Base


class ConversationModel(Base):
    """ORM row for a conversation. Pure persistence concern — kept separate from
    the domain `Conversation` aggregate and bridged by a mapper."""

    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    messages: Mapped[list[MessageModel]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="MessageModel.created_at",
        lazy="selectin",
    )
