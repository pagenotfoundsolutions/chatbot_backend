import uuid
from sqlalchemy import String, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy import Index

from app.shared.database.core_model import CoreModelMixin
from app.shared.database.database import Base

class DocumentChunkModel(CoreModelMixin, Base):
    __tablename__ = "document_chunks"

    file_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), index=True, nullable=False)
    auth_user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), index=True, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    page_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(384), nullable=False)
    content_tsvector = mapped_column(TSVECTOR, nullable=True)

    __table_args__ = (
        Index('ix_document_chunks_content_tsvector', 'content_tsvector', postgresql_using='gin'),
    )
