import uuid
from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, status, BackgroundTasks
from app.modules.files.adapters.input.http.api.schemas import FileResponse
from app.modules.files.application.ports.input.upload_file_use_case import UploadFileUseCase, UploadFileCommand
from app.modules.files.adapters.input.http.api.dependencies import get_upload_file_use_case, get_list_files_use_case, get_download_file_use_case
from app.shared.security.dependencies import get_current_user_id
from app.modules.files.application.ports.input.list_files_use_case import ListFilesUseCase, ListFilesQuery
from app.modules.files.application.ports.input.download_file_use_case import DownloadFileUseCase, DownloadFileQuery
from app.modules.rag.adapters.input.http.dependencies import get_index_file_use_case
from app.modules.rag.application.commands.index_file.index_file_command import IndexFileCommand
from app.modules.rag.application.commands.index_file.index_file_handler import IndexFileHandler
from app.shared.pagination import Page
from fastapi.responses import StreamingResponse
from app.shared.resp import SuccessResp

router = APIRouter()


@router.post("/upload", response_model=SuccessResp[FileResponse], status_code=status.HTTP_201_CREATED)
def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = FastAPIFile(...),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    upload_file_use_case: UploadFileUseCase = Depends(get_upload_file_use_case),
    index_file_use_case: IndexFileHandler = Depends(get_index_file_use_case),
):
    command = UploadFileCommand(
        auth_user_id=current_user_id,
        filename=file.filename or "uploaded_file",
        mime_type=file.content_type or "application/octet-stream",
        file_obj=file.file
    )
    dto = upload_file_use_case.execute(command)
    
    # Trigger RAG indexing in the background
    index_cmd = IndexFileCommand(file_id=dto.id, auth_user_id=dto.auth_user_id)
    background_tasks.add_task(index_file_use_case.execute, index_cmd)
    
    file_response = FileResponse(
        id=dto.id,
        auth_user_id=dto.auth_user_id,
        original_filename=dto.original_filename,
        mime_type=dto.mime_type,
        size_bytes=dto.size_bytes,
        status=dto.status,
        error_message=dto.error_message,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
        file_path=dto.storage_path
    )
    return SuccessResp(message="File uploaded successfully", data=file_response)

@router.get("", response_model=SuccessResp[Page[FileResponse]], status_code=status.HTTP_200_OK)
def list_files(
    page: int = 1,
    size: int = 50,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    list_files_use_case: ListFilesUseCase = Depends(get_list_files_use_case),
):
    query = ListFilesQuery(
        auth_user_id=current_user_id,
        page=page,
        size=size
    )
    dto_page = list_files_use_case.execute(query)
    
    responses = [
        FileResponse(
            id=dto.id,
            auth_user_id=dto.auth_user_id,
            original_filename=dto.original_filename,
            mime_type=dto.mime_type,
            size_bytes=dto.size_bytes,
            status=dto.status,
            error_message=dto.error_message,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            file_path=dto.storage_path
        ) for dto in dto_page.items
    ]
    
    page_data = Page.create(
        items=responses, 
        total=dto_page.total, 
        page=dto_page.page, 
        size=dto_page.size
    )
    return SuccessResp(message="Files retrieved successfully", data=page_data)

@router.get("/{file_path:path}", response_class=StreamingResponse, status_code=status.HTTP_200_OK)
def download_file(
    file_path: str,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    download_file_use_case: DownloadFileUseCase = Depends(get_download_file_use_case),
):
    query = DownloadFileQuery(auth_user_id=current_user_id, file_path=file_path)
    result = download_file_use_case.execute(query)
    
    headers = {
        "Content-Disposition": f'attachment; filename="{result.file_dto.original_filename}"'
    }
    
    return StreamingResponse(
        result.stream, 
        media_type=result.file_dto.mime_type, 
        headers=headers
    )
