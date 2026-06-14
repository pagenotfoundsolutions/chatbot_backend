from __future__ import annotations

from fastapi import APIRouter

from app.modules.chat.adapters.input.http.routes import router as chat_router
from app.shared.presentation.index import router as index_router
from app.modules.auth.adapters.input.http.controller import router as auth_router
from app.modules.profile.adapters.input.http.controller import router as profile_router
# Central place to register EVERY module's router.
# New feature -> add one include_router line here. Don't touch main.py.


def build_api_router() -> APIRouter:
    api_router = APIRouter()
    api_router.include_router(index_router, tags=["index"])
    api_router.include_router(auth_router, tags=["auth"])
    api_router.include_router(chat_router, tags=["chat"])
    api_router.include_router(profile_router, tags=["profile"])
    return api_router
