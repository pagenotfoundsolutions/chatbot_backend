from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.chat.adapters.output.persistence.conversation_mapper import (
    ConversationMapper,
)
from app.modules.chat.adapters.output.persistence.models.conversation_model import (
    ConversationModel,
)
from app.modules.chat.application.ports.output.conversation_repository_port import (
    ConversationRepositoryPort,
)
from app.modules.chat.domain.entities.conversation import Conversation


class SqlAlchemyConversationRepository(ConversationRepositoryPort):
    """SQLAlchemy-backed driven adapter implementing the repository port.

    The unit-of-work is the request-scoped `Session` (injected via FastAPI's
    `get_db`); this adapter owns the commit boundary for chat writes.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, aggregate: Conversation) -> None:
        model = self._session.get(ConversationModel, aggregate.id)

        if model is None:
            model = ConversationModel(
                id=aggregate.id,
                title=aggregate.title,
                created_at=aggregate.created_at,
                updated_at=aggregate.updated_at,
            )
            self._session.add(model)
        else:
            model.title = aggregate.title
            model.updated_at = aggregate.updated_at

        # Append only messages not already persisted (the aggregate may carry
        # both existing and brand-new turns). Identity is the message id.
        existing_ids = {m.id for m in model.messages}
        for message in aggregate.messages:
            if message.id not in existing_ids:
                model.messages.append(
                    ConversationMapper.message_to_model(message, aggregate.id)
                )

    def get(self, id: str) -> Conversation | None:
        model = self._session.get(ConversationModel, id)
        return ConversationMapper.to_domain(model) if model is not None else None

    def list(self) -> list[Conversation]:
        stmt = select(ConversationModel).order_by(ConversationModel.updated_at.desc())
        models = self._session.execute(stmt).scalars().all()
        return [ConversationMapper.to_domain(m) for m in models]

    def delete(self, id: str) -> None:
        model = self._session.get(ConversationModel, id)
        if model is not None:
            self._session.delete(model)
