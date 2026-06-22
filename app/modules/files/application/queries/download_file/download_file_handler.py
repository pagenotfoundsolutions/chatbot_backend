from app.modules.files.application.ports.input.download_file_use_case import (
    DownloadFileUseCase,
    DownloadFileQuery,
    DownloadFileResult,
)
from app.modules.files.application.ports.output.file_repository_port import FileRepositoryPort
from app.modules.files.application.ports.output.file_storage_port import FileStoragePort
from app.modules.files.application.dto.file_dto import FileDTO
from app.shared.exceptions.exceptions import NotFoundException, UnauthorizedException

class DownloadFileHandler(DownloadFileUseCase):
    def __init__(self, repository: FileRepositoryPort, storage: FileStoragePort):
        self._repository = repository
        self._storage = storage

    def execute(self, query: DownloadFileQuery) -> DownloadFileResult:
        file = self._repository.get_by_storage_path(query.file_path)
        if not file:
            raise NotFoundException("File not found")
            
        if file.auth_user_id != query.auth_user_id:
            raise UnauthorizedException("You do not have permission to access this file")
            
        stream = self._storage.get_stream(file.storage_path)
        if stream is None:
            raise NotFoundException("File content not found on physical storage")
        
        return DownloadFileResult(
            file_dto=FileDTO.from_entity(file),
            stream=stream
        )
