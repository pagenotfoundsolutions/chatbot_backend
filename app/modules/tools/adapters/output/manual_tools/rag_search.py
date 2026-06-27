import uuid

from langchain_core.tools import BaseTool, tool
from app.modules.rag.application.ports.input.search_chunks_use_case import SearchChunksUseCase
from app.modules.rag.application.queries.search_chunks.search_chunks_query import SearchChunksQuery

def build_rag_tool(
    auth_user_id: uuid.UUID | None = None,
    file_id: uuid.UUID | None = None,
    search_chunks_use_case: SearchChunksUseCase | None = None
) -> BaseTool:
    """Builds a LangChain tool for searching documents with the given context."""
    
    @tool
    def search_document(query: str) -> str:
        """Searches the user's uploaded document for relevant information to answer their question."""
        if not auth_user_id or not file_id or not search_chunks_use_case:
            return "Error: Missing document context to perform search."
            
        search_query = SearchChunksQuery(
            text=query,
            auth_user_id=auth_user_id,
            file_id=file_id,
            top_k=3
        )
        try:
            chunks = search_chunks_use_case.execute(search_query)
            return "\n\n".join([f"Document Chunk:\n{c.content}" for c in chunks]) if chunks else "No relevant information found in the document."
        except Exception:
            return "Failed to search document due to an internal error."

    return search_document
