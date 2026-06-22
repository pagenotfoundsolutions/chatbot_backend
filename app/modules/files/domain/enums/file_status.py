from enum import Enum

class FileStatus(str, Enum):
    """Lifecycle status of an uploaded file."""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    PARSED = "PARSED"
    ERROR = "ERROR"
