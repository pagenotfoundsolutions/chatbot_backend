from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID

from app.modules.auth.adapters.output.security.jwt_token_generator import PyJwtTokenGenerator
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidTokenException

# We instantiate the generator here to use its verification logic without depending on auth HTTP layer.
token_generator = PyJwtTokenGenerator()
# Set auto_error=False so we can throw our own domain exception if it's missing
security = HTTPBearer(auto_error=False)

def get_current_user_id(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> UUID:
    """
    Extracts and validates the current user's ID from the Authorization header.
    Shared across all modules that require authentication.
    """
    if not credentials:
        raise InvalidTokenException("Missing or invalid authentication credentials.")
        
    token = credentials.credentials
    
    # Let InvalidTokenException bubble up so the global app_exception_handler
    # catches it and formats it automatically as an ErrorResp
    payload = token_generator.verify_access_token(token)
    return UUID(payload["sub"])
