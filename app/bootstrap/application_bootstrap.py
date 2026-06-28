from __future__ import annotations

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError

from app.bootstrap.dependency_container import get_container
from app.bootstrap.route_registry import build_api_router
from app.shared.database.init_db import init_db
from app.shared.exceptions.exception_handlers import (
    app_exception_handler, 
    validation_exception_handler, 
    general_exception_handler,
    integrity_exception_handler
)
from app.shared.exceptions.exceptions import AppException


def create_app() -> FastAPI:
    """FastAPI application factory — the single bootstrap entry point.

    Wires everything the monolith needs to serve requests: schema creation,
    metadata, global error handling, and every module's routes. main.py just
    calls this.
    """
    container = get_container()
    settings = container.settings

    # Create all tables registered on Base.metadata.
    init_db()

    app = FastAPI(
        title=settings.project_name,
        description=settings.description,
        version=settings.version,
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Map every domain/application AppException to a uniform ErrorResp payload.
    app.add_exception_handler(AppException, app_exception_handler)
    
    # Override FastAPI's default Pydantic validation error handler
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    
    # Catch SQLAlchemy IntegrityErrors (like foreign key violations)
    app.add_exception_handler(IntegrityError, integrity_exception_handler)

    # Catch any unhandled 500 internal server errors so they return JSON, not plain text
    app.add_exception_handler(Exception, general_exception_handler)

    app.include_router(build_api_router(), prefix="/api")

    return app
