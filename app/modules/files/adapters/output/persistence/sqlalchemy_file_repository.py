import uuid
from typing import Optional
from sqlalchemy import select, func, update
from sqlalchemy.orm import Session

from app.modules.files.application.ports.output.file_repository_port import FileRepositoryPort
from app.modules.files.domain.entities.file import File
from app.modules.files.adapters.output.persistence.models.file_model import FileModel
from app.modules.files.adapters.output.persistence.file_mapper import FileMapper


class SqlAlchemyFileRepository(FileRepositoryPort):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, file: File) -> None:
        db_file = FileMapper.to_persistence(file)
        self._session.merge(db_file)
        self._session.commit()

    def get(self, id: uuid.UUID) -> Optional[File]:
        db_file = self._session.get(FileModel, id)
        if db_file:
            return FileMapper.to_domain(db_file)
        return None

    def get_by_user_and_hash(self, auth_user_id: uuid.UUID, file_hash: str) -> Optional[File]:
        stmt = select(FileModel).where(
            FileModel.auth_user_id == auth_user_id,
            FileModel.file_hash == file_hash
        )
        db_file = self._session.scalar(stmt)
        if db_file:
            return FileMapper.to_domain(db_file)
        return None

    def get_by_storage_path(self, storage_path: str) -> Optional[File]:
        stmt = select(FileModel).where(FileModel.storage_path == storage_path)
        db_file = self._session.scalar(stmt)
        if db_file:
            return FileMapper.to_domain(db_file)
        return None

    def list_by_user(self, auth_user_id: uuid.UUID, page: int, size: int) -> tuple[list[File], int]:
        total = self._session.scalar(
            select(func.count()).select_from(FileModel).where(FileModel.auth_user_id == auth_user_id)
        ) or 0
        
        stmt = select(FileModel).where(
            FileModel.auth_user_id == auth_user_id
        ).order_by(FileModel.created_at.desc()).offset((page - 1) * size).limit(size)
        
        models = self._session.execute(stmt).scalars().all()
        return [FileMapper.to_domain(m) for m in models], total

    def delete(self, id: uuid.UUID) -> None:
        stmt = update(FileModel).where(FileModel.id == id).values(deleted_at=func.now())
        self._session.execute(stmt)

    def get_many_by_ids(self, ids: list[uuid.UUID]) -> list[File]:
        if not ids:
            return []
        stmt = select(FileModel).where(FileModel.id.in_(ids))
        models = self._session.scalars(stmt).all()
        return [FileMapper.to_domain(m) for m in models]
