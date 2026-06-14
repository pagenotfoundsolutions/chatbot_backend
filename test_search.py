from app.models.chunk import Chunk
from app.services.vector_search import search_chunks

chunks = [
    Chunk(
        chunk_id=1,
        content="FastAPI is a web framework"
    ),
    Chunk(
        chunk_id=2,
        content="Python supports OOP"
    ),
    Chunk(
        chunk_id=3,
        content="FAISS is used for vector search"
    )
]

results = search_chunks(
    query="backend  web framework",
    chunks=chunks
)

for score, chunk in results:
    print(score, chunk.content)