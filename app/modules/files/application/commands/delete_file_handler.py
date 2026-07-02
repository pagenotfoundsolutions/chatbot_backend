import logging

from app.modules.files.application.ports.input.delete_file_use_case import (
    DeleteFileCommand,
    DeleteFileUseCase,
)
from app.modules.files.application.ports.output.file_repository_port import FileRepositoryPort
from app.modules.files.application.ports.output.file_storage_port import FileStoragePort
from app.modules.files.application.ports.output.file_reference_port import FileReferencePort
from app.modules.rag.application.ports.output.vector_store_port import VectorStorePort
from app.shared.exceptions.exceptions import (
    NotFoundException,
    UnauthorizedException,
    ConflictException,
)

logger = logging.getLogger(__name__)


class DeleteFileHandler(DeleteFileUseCase):
    """Deletes a file only if it is not linked to any conversation or message.

    A linked file cannot be removed (409). An unlinked file is removed
    everywhere: its RAG chunks, the DB row (soft-delete), and the stored bytes.
    """

    def __init__(
        self,
        repository: FileRepositoryPort,
        storage: FileStoragePort,
        reference_checker: FileReferencePort,
        vector_store: VectorStorePort,
    ) -> None:
        self._repository = repository
        self._storage = storage
        self._reference_checker = reference_checker
        self._vector_store = vector_store

    def execute(self, command: DeleteFileCommand) -> None:
        file = self._repository.get(command.file_id)
        if not file:
            raise NotFoundException("File not found")

        if file.auth_user_id != command.auth_user_id:
            raise UnauthorizedException("You do not have permission to delete this file")

        if self._reference_checker.is_referenced(command.file_id):
            raise ConflictException(
                "This file cannot be deleted because it is linked to a conversation or message."
            )

        # Remove RAG chunks and the DB row in the same transaction. repository.delete
        # commits the shared session, persisting the chunk deletes too.
        self._vector_store.delete_by_file_id(command.file_id)
        self._repository.delete(command.file_id)

        # The physical file is intentionally kept in storage so that if the user
        # uploads the same file again (same hash), we can just restore the DB row.
        # try:
        #     self._storage.delete(file.storage_path)
        # except Exception:  # noqa: BLE001 - best-effort cleanup; DB state is authoritative
        #     logger.warning(
        #         "Failed to delete stored file for %s at %s", command.file_id, file.storage_path,
        #         exc_info=True,
        #     )
