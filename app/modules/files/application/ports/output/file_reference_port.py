from abc import ABC, abstractmethod
import uuid


class FileReferencePort(ABC):
    """Outbound port to check whether a file is still linked to other aggregates.

    A file may only be deleted while nothing references it. This port lets the
    files module ask that question without depending on the chat module's models.
    """

    @abstractmethod
    def is_referenced(self, file_id: uuid.UUID) -> bool:
        """Return True if the file is attached to any conversation or message."""
        ...
