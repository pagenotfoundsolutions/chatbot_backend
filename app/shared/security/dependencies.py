from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID

from app.modules.auth.adapters.output.security.jwt_token_generator import PyJwtTokenGenerator
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidTokenException

# We instantiate the generator here to use its verification logic without depending on auth HTTP layer.
token_generator = PyJwtTokenGenerator()
security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UUID:
    """
    Extracts and validates the current user's ID from the Authorization header.
    Shared across all modules that require authentication.
    """
    token = credentials.credentials
    try:
        payload = token_generator.verify_access_token(token)
        return UUID(payload["sub"])
    except InvalidTokenException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
