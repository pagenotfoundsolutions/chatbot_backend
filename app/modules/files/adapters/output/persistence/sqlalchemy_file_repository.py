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
        db_file = self._session.get(FileModel, file.id, execution_options={"include_deleted": True})
        if db_file:
            db_file.status = file.status
            db_file.error_message = file.error_message
            db_file.updated_at = file.updated_at
            if file.is_deleted and db_file.deleted_at is None:
                db_file.deleted_at = func.now()
        else:
            db_file = FileMapper.to_persistence(file)
            self._session.add(db_file)
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
        ).execution_options(include_deleted=True)
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
        self._session.commit()

    def undelete(self, id: uuid.UUID) -> None:
        stmt = update(FileModel).where(FileModel.id == id).values(deleted_at=None)
        self._session.execute(stmt)
        self._session.commit()

    def get_many_by_ids(self, ids: list[uuid.UUID]) -> list[File]:
        if not ids:
            return []
        stmt = select(FileModel).where(FileModel.id.in_(ids))
        models = self._session.scalars(stmt).all()
        return [FileMapper.to_domain(m) for m in models]
