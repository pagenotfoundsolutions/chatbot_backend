from __future__ import annotations

import uuid
from datetime import datetime

from app.modules.chat.domain.entities.message import Message
from app.modules.chat.domain.events.message_posted import MessagePosted
from app.modules.chat.domain.value_objects.message_role import MessageRole
from app.shared.kernel.aggregate_root import AggregateRoot

_DEFAULT_TITLE = "New chat"


from app.shared.kernel.utils import generate_uuid, utc_now


class Conversation(AggregateRoot[uuid.UUID]):
    """Aggregate root for a chat.

    All message mutations go THROUGH this root so the aggregate stays consistent
    (`updated_at` always reflects the last activity) and so each append records a
    `MessagePosted` domain event. Nothing outside the domain appends to
    `messages` directly.
    """

    def __init__(
        self,
        id: uuid.UUID,
        auth_user_id: uuid.UUID,
        title: str,
        created_at: datetime,
        updated_at: datetime,
        messages: list[Message] | None = None,
    ) -> None:
        super().__init__(id)
        self._auth_user_id = auth_user_id
        self._title = title
        self._created_at = created_at
        self._updated_at = updated_at
        self._messages: list[Message] = list(messages) if messages else []

    # --- factory -----------------------------------------------------------
    @classmethod
    def start(cls, auth_user_id: uuid.UUID, title: str | None = None) -> "Conversation":
        """Open a brand-new, empty conversation."""
        now = utc_now()
        clean = (title or "").strip() or _DEFAULT_TITLE
        return cls(id=generate_uuid(), auth_user_id=auth_user_id, title=clean, created_at=now, updated_at=now)

    # --- read-only state ---------------------------------------------------
    @property
    def auth_user_id(self) -> uuid.UUID:
        return self._auth_user_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def messages(self) -> tuple[Message, ...]:
        # tuple -> callers cannot mutate the internal list.
        return tuple(self._messages)

    # --- behaviour ---------------------------------------------------------
    def rename(self, title: str) -> None:
        clean = (title or "").strip()
        if not clean:
            raise ValueError("Conversation title cannot be empty")
        self._title = clean
        self._touch()

    def post_user_message(self, content: str) -> Message:
        return self._append(MessageRole.USER, content)

    def post_assistant_message(self, content: str) -> Message:
        return self._append(MessageRole.ASSISTANT, content)

    def post_system_message(self, content: str) -> Message:
        return self._append(MessageRole.SYSTEM, content)

    # --- internals ---------------------------------------------------------
    def _append(self, role: MessageRole, content: str) -> Message:
        new_msg = Message.create(role=role, content=content)
        self._messages.append(new_msg)
        self._touch()
        self.record(
            MessagePosted(
                conversation_id=self.id,
                message_id=new_msg.id,
                role=role,
            )
        )
        return new_msg

    def _touch(self) -> None:
        self._updated_at = utc_now()
