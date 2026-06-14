from pathlib import Path

from app.services.pdf_reader import read_pdf
from app.services.text_splitter import text_splitter

pdf_path = Path(
    "uploads/a4b92ae9-05e5-455e-814c-e67dec223d70.pdf"
)

text = read_pdf(pdf_path)

chunks = text_splitter(text,chunk_size=50,chunk_overlap=10)

print(f"Total Chunks: {len(chunks)}")

print("\n")

print(chunks)