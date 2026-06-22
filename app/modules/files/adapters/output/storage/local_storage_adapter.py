import os
import shutil
from pathlib import Path
from typing import BinaryIO, Optional

from app.modules.files.application.ports.output.file_storage_port import (
    FileStoragePort,
)


class LocalStorageAdapter(FileStoragePort):
    """Adapter for saving files to the local file system (or Docker volume)."""

    def __init__(self, upload_dir: str) -> None:
        self.upload_dir = Path(upload_dir)
        # Ensure the directory exists when instantiated
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save(self, filename: str, content: BinaryIO) -> str:
        file_path = self.upload_dir / filename
        
        # Ensure parent directories exist (in case filename contains slashes)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(content, f)
            
        # Return the relative filename instead of absolute/base path
        return filename

    def delete(self, storage_path: str) -> None:
        path = self.upload_dir / storage_path
        if path.exists():
            path.unlink()

    def get_stream(self, storage_path: str) -> Optional[BinaryIO]:
        path = self.upload_dir / storage_path
        if not path.exists():
            return None
        return open(path, "rb")
