import os
from typing import Sequence
import pandas as pd
from PIL import Image
import pytesseract

from langchain_community.document_loaders import (
    PyPDFLoader, 
    TextLoader, 
    Docx2txtLoader, 
    CSVLoader,
    BSHTMLLoader
)
from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter, 
    Language,
    MarkdownTextSplitter
)

from app.modules.rag.application.ports.output.document_processor_port import DocumentProcessorPort
from app.modules.rag.application.dto.chunk_dto import ChunkDTO

CODE_EXTENSIONS = {
    # Basic
    ".py": Language.PYTHON,
    ".js": Language.JS,
    ".ts": Language.TS,
    ".go": Language.GO,
    ".cpp": Language.CPP,
    ".c": Language.C,
    ".java": Language.JAVA,
    ".rs": Language.RUST,
    ".rb": Language.RUBY,
    ".php": Language.PHP,
    ".html": Language.HTML,
    # Extended
    ".cs": Language.CSHARP,
    ".kt": Language.KOTLIN,
    ".kts": Language.KOTLIN,
    ".swift": Language.SWIFT,
    ".scala": Language.SCALA,
    ".r": Language.R,
    ".rst": Language.RST,
    ".tex": Language.LATEX,
    ".latex": Language.LATEX,
    ".sol": Language.SOL,
    ".cob": Language.COBOL,
    ".cbl": Language.COBOL,
    ".lua": Language.LUA,
    ".pl": Language.PERL,
    ".pm": Language.PERL,
    ".hs": Language.HASKELL,
    ".ex": Language.ELIXIR,
    ".exs": Language.ELIXIR,
    ".ps1": Language.POWERSHELL,
    ".bas": Language.VISUALBASIC6,
    ".vba": Language.VISUALBASIC6,
    ".vbs": Language.VISUALBASIC6,
    ".proto": Language.PROTO,
}

class LangchainDocumentProcessorAdapter(DocumentProcessorPort):
    def extract_and_chunk(self, file_path: str, mime_type: str) -> Sequence[ChunkDTO]:
        _, ext = os.path.splitext(file_path.lower())
        docs = []

        # 1. Select Loader based on extension or mime_type
        if ext == ".pdf" or mime_type == "application/pdf":
            loader = PyPDFLoader(file_path)
            docs = loader.load()
        elif ext in [".docx", ".doc"]:
            loader = Docx2txtLoader(file_path)
            docs = loader.load()
        elif ext == ".csv" or mime_type == "text/csv":
            loader = CSVLoader(file_path=file_path)
            docs = loader.load()
        elif ext in [".xlsx", ".xls"]:
            # Custom Pandas loader for Excel
            df = pd.read_excel(file_path)
            csv_path = file_path + ".csv"
            df.to_csv(csv_path, index=False)
            loader = CSVLoader(file_path=csv_path)
            docs = loader.load()
            if os.path.exists(csv_path):
                os.remove(csv_path)
        elif ext in [".png", ".jpg", ".jpeg"]:
            # Custom Image OCR Loader
            text = pytesseract.image_to_string(Image.open(file_path))
            docs = [Document(page_content=text, metadata={"source": file_path, "page": 1})]
        elif ext in [".htm", ".html"]:
            loader = BSHTMLLoader(file_path)
            docs = loader.load()
        else:
            # Fallback to TextLoader for Code, Markdown, TXT, JSON, etc.
            loader = TextLoader(file_path)
            try:
                docs = loader.load()
            except Exception as e:
                # If utf-8 fails, try with autodetect or latin-1
                loader = TextLoader(file_path, encoding="latin-1")
                docs = loader.load()

        # 2. Select Splitter based on extension
        if ext == ".md":
            text_splitter = MarkdownTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                add_start_index=True
            )
        elif ext in CODE_EXTENSIONS:
            language = CODE_EXTENSIONS[ext]
            text_splitter = RecursiveCharacterTextSplitter.from_language(
                language=language,
                chunk_size=1000,
                chunk_overlap=200,
                add_start_index=True
            )
        else:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                add_start_index=True
            )

        # 3. Split Documents
        split_docs = text_splitter.split_documents(docs)

        # 4. Map to ChunkDTO
        chunks = []
        for doc in split_docs:
            page_num = doc.metadata.get("page")
            if page_num is not None:
                # Only increment if it's 0-indexed like PyPDF
                if ext == ".pdf":
                    page_num += 1
            else:
                page_num = 1
                
            chunks.append(ChunkDTO(content=doc.page_content, page_number=page_num))
            
        return chunks
