from fastapi import APIRouter

from app.shared.config.settings import settings

router = APIRouter()


@router.get("/")
def index():
    return {
        "name": settings.name,
        "description": settings.description,
        "version": settings.version,
    }
