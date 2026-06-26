from pydantic import BaseModel
from typing import Optional

class ChunkDTO(BaseModel):
    content: str
    page_number: Optional[int] = None
