from fastapi import APIRouter
from app.modules.files.adapters.input.http.api.controller import router as files_router

def register_routes(api_router: APIRouter):
    api_router.include_router(files_router, prefix="/files", tags=["Files"])
