import uuid
from sqlalchemy import String, Integer, Enum, Uuid, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.database import Base
from app.shared.database.core_model import CoreModelMixin
from app.modules.files.domain.enums.file_status import FileStatus


class FileModel(CoreModelMixin, Base):
    __tablename__ = "files"
    __table_args__ = (
        UniqueConstraint("auth_user_id", "file_hash", name="uq_auth_user_id_file_hash"),
    )

    auth_user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("auth_users.id", ondelete="CASCADE"), nullable=False, index=True)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_filename: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    mime_type: Mapped[str] = mapped_column(String(255), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    storage_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    file_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    status: Mapped[FileStatus] = mapped_column(Enum(FileStatus), nullable=False, default=FileStatus.PENDING)
    error_message: Mapped[str | None] = mapped_column(String, nullable=True)
