from fastapi import Depends
from sqlalchemy.orm import Session

from app.bootstrap.dependency_container import get_container, DependencyContainer
from app.shared.database.session import get_db
from app.modules.files.adapters.output.persistence.sqlalchemy_file_repository import SqlAlchemyFileRepository
from app.modules.files.adapters.output.storage.local_storage_adapter import LocalStorageAdapter
from app.modules.files.application.ports.input.upload_file_use_case import UploadFileUseCase
from app.modules.files.application.commands.upload_file_handler import UploadFileHandler
from app.modules.files.application.ports.input.list_files_use_case import ListFilesUseCase
from app.modules.files.application.ports.input.download_file_use_case import DownloadFileUseCase
from app.modules.files.application.ports.input.delete_file_use_case import DeleteFileUseCase
from app.modules.files.application.ports.input.get_file_detail_use_case import GetFileDetailUseCase
from app.modules.files.adapters.output.persistence.sqlalchemy_file_reference_checker import (
    SqlAlchemyFileReferenceChecker,
)


def get_file_repository(db: Session = Depends(get_db)) -> SqlAlchemyFileRepository:
    return SqlAlchemyFileRepository(session=db)


def get_file_reference_checker(db: Session = Depends(get_db)) -> SqlAlchemyFileReferenceChecker:
    return SqlAlchemyFileReferenceChecker(session=db)


def get_file_storage(container: DependencyContainer = Depends(get_container)) -> LocalStorageAdapter:
    return LocalStorageAdapter(upload_dir=container.settings.upload_dir)


def get_upload_file_use_case(
    repo: SqlAlchemyFileRepository = Depends(get_file_repository),
    storage: LocalStorageAdapter = Depends(get_file_storage),
) -> UploadFileUseCase:
    return UploadFileHandler(repository=repo, storage=storage)


def get_list_files_use_case(
    repo: SqlAlchemyFileRepository = Depends(get_file_repository),
) -> ListFilesUseCase:
    from app.modules.files.application.queries.list_files.list_files_handler import ListFilesHandler
    return ListFilesHandler(repository=repo)


def get_download_file_use_case(
    repo: SqlAlchemyFileRepository = Depends(get_file_repository),
    storage: LocalStorageAdapter = Depends(get_file_storage),
) -> DownloadFileUseCase:
    from app.modules.files.application.queries.download_file.download_file_handler import DownloadFileHandler
    return DownloadFileHandler(repository=repo, storage=storage)


def get_file_detail_use_case(
    repo: SqlAlchemyFileRepository = Depends(get_file_repository),
) -> GetFileDetailUseCase:
    from app.modules.files.application.queries.get_file_detail.get_file_detail_handler import GetFileDetailHandler
    return GetFileDetailHandler(repository=repo)


def get_delete_file_use_case(
    db: Session = Depends(get_db),
    repo: SqlAlchemyFileRepository = Depends(get_file_repository),
    storage: LocalStorageAdapter = Depends(get_file_storage),
    reference_checker: SqlAlchemyFileReferenceChecker = Depends(get_file_reference_checker),
) -> DeleteFileUseCase:
    # Lazy import of the RAG vector store to avoid a circular import between the
    # files and rag dependency modules (rag imports get_file_repository from here).
    from app.modules.rag.adapters.input.http.dependencies import get_vector_store_port
    from app.modules.files.application.commands.delete_file_handler import DeleteFileHandler

    vector_store = get_vector_store_port(db=db)
    return DeleteFileHandler(
        repository=repo,
        storage=storage,
        reference_checker=reference_checker,
        vector_store=vector_store,
    )
