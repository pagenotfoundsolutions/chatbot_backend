import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.modules.files.application.ports.output.file_reference_port import FileReferencePort


class SqlAlchemyFileReferenceChecker(FileReferencePort):
    """Checks the chat tables for any reference to a file.

    Uses raw SQL against the table names so the files module stays decoupled
    from the chat module's ORM classes and avoids a circular import. Raw SQL
    also bypasses the global soft-delete filter on purpose: a file linked to a
    soft-deleted conversation/message is still considered "in use".
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def is_referenced(self, file_id: uuid.UUID) -> bool:
        fid = str(file_id)

        attached = self._session.execute(
            text("SELECT 1 FROM conversation_files WHERE file_id = :fid LIMIT 1"),
            {"fid": fid},
        ).first()
        if attached is not None:
            return True

        in_message = self._session.execute(
            text("SELECT 1 FROM messages WHERE file_id = :fid LIMIT 1"),
            {"fid": fid},
        ).first()
        return in_message is not None
