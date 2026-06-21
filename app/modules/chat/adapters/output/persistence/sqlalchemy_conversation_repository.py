from __future__ import annotations
import uuid

from sqlalchemy import select, func, update
from sqlalchemy.orm import Session, noload

from app.modules.chat.adapters.output.persistence.conversation_mapper import (
    ConversationMapper,
)
from app.modules.chat.adapters.output.persistence.models.conversation_model import (
    ConversationModel,
)
from app.modules.chat.adapters.output.persistence.models.message_model import (
    MessageModel,
)
from app.modules.chat.application.ports.output.conversation_repository_port import (
    ConversationRepositoryPort,
)
from app.modules.chat.domain.entities.conversation import Conversation
from app.modules.chat.domain.entities.message import Message


class SqlAlchemyConversationRepository(ConversationRepositoryPort):
    """SQLAlchemy-backed driven adapter implementing the repository port.

    The unit-of-work is the request-scoped `Session` (injected via FastAPI's
    `get_db`); this adapter owns the commit boundary for chat writes.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, aggregate: Conversation) -> None:
        exists = self._session.scalar(select(ConversationModel.id).where(ConversationModel.id == aggregate.id))

        if not exists:
            model = ConversationModel(
                id=aggregate.id,
                auth_user_id=aggregate.auth_user_id,
                title=aggregate.title,
                created_at=aggregate.created_at,
                updated_at=aggregate.updated_at,
            )
            self._session.add(model)
        else:
            stmt = update(ConversationModel).where(ConversationModel.id == aggregate.id).values(
                title=aggregate.title,
                updated_at=aggregate.updated_at
            )
            self._session.execute(stmt)

        existing_ids = set(self._session.scalars(select(MessageModel.id).where(MessageModel.conversation_id == aggregate.id)).all())
        new_messages = [
            ConversationMapper.message_to_model(message, aggregate.id)
            for message in aggregate.messages if message.id not in existing_ids
        ]
        if new_messages:
            self._session.add_all(new_messages)

    def get(self, id: uuid.UUID) -> Conversation | None:
        model = self._session.get(ConversationModel, id)
        return ConversationMapper.to_domain(model) if model is not None else None

    def list(self, auth_user_id: uuid.UUID, page: int, size: int) -> tuple[list[Conversation], int]:
        total = self._session.scalar(
            select(func.count()).select_from(ConversationModel).where(ConversationModel.auth_user_id == auth_user_id)
        ) or 0
        
        stmt = select(ConversationModel).where(
            ConversationModel.auth_user_id == auth_user_id
        ).order_by(ConversationModel.updated_at.desc()).offset((page - 1) * size).limit(size)
        
        stmt = stmt.options(noload(ConversationModel.messages))
        models = self._session.execute(stmt).scalars().all()
        return [ConversationMapper.to_domain(m) for m in models], total

    def list_messages(self, conversation_id: uuid.UUID, auth_user_id: uuid.UUID, page: int, size: int) -> tuple[list[Message], int] | None:
        exists = self._session.scalar(
            select(ConversationModel.id).where(ConversationModel.id == conversation_id, ConversationModel.auth_user_id == auth_user_id)
        )
        if not exists:
            return None
            
        total = self._session.scalar(
            select(func.count()).select_from(MessageModel).where(MessageModel.conversation_id == conversation_id)
        ) or 0
        
        stmt = select(MessageModel).where(
            MessageModel.conversation_id == conversation_id
        ).order_by(MessageModel.created_at.asc()).offset((page - 1) * size).limit(size)
        
        models = self._session.execute(stmt).scalars().all()
        return [ConversationMapper.message_to_domain(m) for m in models], total

    def delete(self, id: uuid.UUID) -> None:
        stmt = update(ConversationModel).where(ConversationModel.id == id).values(deleted_at=func.now())
        self._session.execute(stmt)
