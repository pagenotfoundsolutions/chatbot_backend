from app.modules.files.application.dto.file_dto import FileDTO
from app.modules.files.application.ports.input.get_file_detail_use_case import (
    GetFileDetailQuery,
    GetFileDetailUseCase,
)
from app.modules.files.application.ports.output.file_repository_port import FileRepositoryPort
from app.shared.exceptions.exceptions import NotFoundException, UnauthorizedException


class GetFileDetailHandler(GetFileDetailUseCase):
    def __init__(self, repository: FileRepositoryPort) -> None:
        self._repository = repository

    def execute(self, query: GetFileDetailQuery) -> FileDTO:
        file = self._repository.get(query.file_id)
        if not file:
            raise NotFoundException("File not found")

        if file.auth_user_id != query.auth_user_id:
            raise UnauthorizedException("You do not have permission to access this file")

        return FileDTO.from_entity(file)
