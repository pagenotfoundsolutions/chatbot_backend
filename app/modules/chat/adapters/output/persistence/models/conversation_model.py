from __future__ import annotations

import uuid
from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

from app.modules.chat.adapters.output.persistence.models.message_model import (
    MessageModel,
)
from app.shared.database.database import Base
from app.shared.database.core_model import CoreModelMixin


class ConversationFileModel(Base):
    __tablename__ = "conversation_files"
    conversation_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), primary_key=True)
    file_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("files.id", ondelete="CASCADE"), primary_key=True)


class ConversationModel(CoreModelMixin, Base):
    """ORM row for a conversation. Pure persistence concern — kept separate from
    the domain `Conversation` aggregate and bridged by a mapper."""

    __tablename__ = "conversations"

    auth_user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("auth_users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    files: Mapped[list[ConversationFileModel]] = relationship(
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    messages: Mapped[list[MessageModel]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="MessageModel.created_at.desc()",
        lazy="selectin",
    )
