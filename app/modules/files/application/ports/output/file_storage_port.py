from abc import ABC, abstractmethod
from typing import BinaryIO, Optional


class FileStoragePort(ABC):
    """Outbound port for physical file storage (Local, S3, etc)."""

    @abstractmethod
    def save(self, filename: str, content: BinaryIO) -> str:
        """
        Save the raw file bytes to storage.
        
        Args:
            filename: The generated secure filename to save as.
            content: A file-like object containing the raw bytes.
            
        Returns:
            str: The relative storage path or URL where the file is stored.
        """
        ...

    @abstractmethod
    def delete(self, storage_path: str) -> None:
        """Remove a file from storage."""
        ...

    @abstractmethod
    def get_stream(self, storage_path: str) -> Optional[BinaryIO]:
        """Get a read-only stream of the file content, or None if the file is missing."""
        ...
