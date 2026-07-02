from app.modules.files.domain.entities.file import File
from app.modules.files.adapters.output.persistence.models.file_model import FileModel


class FileMapper:
    """Maps between File domain entity and FileModel."""

    @staticmethod
    def to_domain(model: FileModel) -> File:
        return File(
            id=model.id,
            auth_user_id=model.auth_user_id,
            original_filename=model.original_filename,
            stored_filename=model.stored_filename,
            mime_type=model.mime_type,
            size_bytes=model.size_bytes,
            storage_path=model.storage_path,
            file_hash=model.file_hash,
            status=model.status,
            error_message=model.error_message,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_deleted=model.deleted_at is not None,
        )

    @staticmethod
    def to_persistence(entity: File) -> FileModel:
        return FileModel(
            id=entity.id,
            auth_user_id=entity.auth_user_id,
            original_filename=entity.original_filename,
            stored_filename=entity.stored_filename,
            mime_type=entity.mime_type,
            size_bytes=entity.size_bytes,
            storage_path=entity.storage_path,
            file_hash=entity.file_hash,
            status=entity.status,
            error_message=entity.error_message,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
        if entity.is_deleted:
            from app.shared.kernel.utils import utc_now
            model.deleted_at = utc_now()
        return model
