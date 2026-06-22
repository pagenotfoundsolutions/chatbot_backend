import hashlib
import os
import uuid

from app.modules.files.application.dto.file_dto import FileDTO
from app.modules.files.application.ports.input.upload_file_use_case import (
    UploadFileCommand,
    UploadFileUseCase,
)
from app.modules.files.application.ports.output.file_repository_port import (
    FileRepositoryPort,
)
from app.modules.files.application.ports.output.file_storage_port import (
    FileStoragePort,
)
from app.modules.files.domain.entities.file import File
from app.modules.files.domain.exceptions.file_exceptions import FileAlreadyExistsError


class UploadFileHandler(UploadFileUseCase):
    """Handles `UploadFileCommand`: saves file to storage and creates metadata."""

    def __init__(
        self, repository: FileRepositoryPort, storage: FileStoragePort
    ) -> None:
        self._repository = repository
        self._storage = storage

    def execute(self, command: UploadFileCommand) -> FileDTO:
        # Read file bytes to calculate hash and size
        file_bytes = command.file_obj.read()
        
        size_bytes = len(file_bytes)
        if size_bytes == 0:
            from app.shared.exceptions.exceptions import ValidationException
            raise ValidationException("File is empty.")

        # Calculate SHA256 hash to prevent duplicates
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        # Check if file with same hash exists for THIS user
        existing_file = self._repository.get_by_user_and_hash(command.auth_user_id, file_hash)
        if existing_file:
            raise FileAlreadyExistsError(existing_file.id)

        # Generate a secure stored filename scoped to the user directory
        # E.g. "auth_user_id/uuid_ext"
        ext = os.path.splitext(command.filename)[1]
        stored_filename = f"{command.auth_user_id}/{uuid.uuid4()}{ext}"

        # We must seek to 0 before saving if the port reads from the file-like object, 
        # but since we already have bytes, we can pass a new BytesIO or let the port take bytes.
        # Let's adjust storage port to accept bytes or BinaryIO. 
        # Wait, the port says `BinaryIO`. Let's just wrap it.
        import io
        byte_stream = io.BytesIO(file_bytes)

        # Save to storage
        storage_path = self._storage.save(stored_filename, byte_stream)

        # Create Domain Entity
        file_entity = File.create(
            auth_user_id=command.auth_user_id,
            original_filename=command.filename,
            stored_filename=stored_filename,
            mime_type=command.mime_type,
            size_bytes=size_bytes,
            storage_path=storage_path,
            file_hash=file_hash,
        )

        # Persist to DB
        self._repository.save(file_entity)

        return FileDTO.from_entity(file_entity)
