from app.modules.files.application.ports.input.list_files_use_case import (
    ListFilesUseCase,
    ListFilesQuery,
)
from app.modules.files.application.ports.output.file_repository_port import FileRepositoryPort
from app.modules.files.application.dto.file_dto import FileDTO
from app.shared.pagination import Page

class ListFilesHandler(ListFilesUseCase):
    def __init__(self, repository: FileRepositoryPort):
        self._repository = repository

    def execute(self, query: ListFilesQuery) -> Page[FileDTO]:
        files, total = self._repository.list_by_user(query.auth_user_id, query.page, query.size)
        
        return Page.create(
            items=[FileDTO.from_entity(f) for f in files],
            total=total,
            page=query.page,
            size=query.size
        )
