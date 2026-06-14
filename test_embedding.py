from app.services.embedding_service import create_embedding

v1 = create_embedding(
    "FastAPI is a web framework"
)

v2 = create_embedding(
    "FastAPI is a backend framework"
)

print(len(v1))
print(len(v2))