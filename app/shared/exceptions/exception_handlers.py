from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.shared.resp import ErrorResp
from .exceptions import AppException

def app_exception_handler(request: Request, exc: AppException):
    resp = ErrorResp(message=exc.message, error=str(exc.__class__.__name__))
    return JSONResponse(
        status_code=exc.status_code,
        content=resp.model_dump()
    )

def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract the first error message from Pydantic's detailed error list
    error_msg = exc.errors()[0].get("msg", "Validation error")
    error_field = exc.errors()[0].get("loc", ["unknown"])[-1]
    
    resp = ErrorResp(
        message=f"Validation failed for '{error_field}': {error_msg}", 
        error="RequestValidationError"
    )
    return JSONResponse(
        status_code=422,
        content=resp.model_dump()
    )

def general_exception_handler(request: Request, exc: Exception):
    # Catch-all for unhandled 500 Internal Server Errors
    resp = ErrorResp(
        message="An unexpected error occurred on the server.", 
        error=str(exc.__class__.__name__)
    )
    return JSONResponse(
        status_code=500,
        content=resp.model_dump()
    )