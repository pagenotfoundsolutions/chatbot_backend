from __future__ import annotations
import uuid

from app.modules.chat.adapters.output.persistence.models.conversation_model import (
    ConversationModel,
)
from app.modules.chat.adapters.output.persistence.models.message_model import (
    MessageModel,
)
from app.modules.chat.domain.entities.conversation import Conversation
from app.modules.chat.domain.entities.message import Message
from app.modules.chat.domain.value_objects.message_role import MessageRole


class ConversationMapper:
    """Translates between the persistence model and the domain aggregate.

    Keeping this at the persistence seam means neither the ORM nor the domain
    knows the other exists — they meet only here.
    """

    @staticmethod
    def message_to_domain(model: MessageModel) -> Message:
        return Message(
            id=model.id,
            role=MessageRole(model.role),
            content=model.content,
            created_at=model.created_at,
            file_id=model.file_id,
        )

    @staticmethod
    def to_domain(model: ConversationModel) -> Conversation:
        return Conversation(
            id=model.id,
            auth_user_id=model.auth_user_id,
            title=model.title,
            created_at=model.created_at,
            updated_at=model.updated_at,
            messages=[
                ConversationMapper.message_to_domain(m) for m in model.messages
            ],
            file_ids={f.file_id for f in model.files},
        )

    @staticmethod
    def message_to_model(message: Message, conversation_id: uuid.UUID) -> MessageModel:
        return MessageModel(
            id=message.id,
            conversation_id=conversation_id,
            role=message.role.value,
            content=message.content,
            created_at=message.created_at,
            file_id=message.file_id,
        )
