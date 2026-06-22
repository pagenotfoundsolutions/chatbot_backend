import uuid

from app.shared.exceptions.exceptions import AppException

class FileAlreadyExistsError(AppException):
    """Raised when a user attempts to upload a file with exactly the same content they already uploaded."""
    def __init__(self, file_id: uuid.UUID):
        self.file_id = file_id
        super().__init__(message=f"File with same content already exists (ID: {file_id})", status_code=409)
