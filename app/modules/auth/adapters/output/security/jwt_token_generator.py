import jwt
from datetime import datetime, timedelta
from typing import Any, Dict
from uuid import UUID
import secrets
from app.modules.auth.application.ports.output.token_generator_port import TokenGeneratorPort
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidTokenException
from app.modules.auth.infrastructure.config.auth_config import get_auth_config

class PyJwtTokenGenerator(TokenGeneratorPort):
    def __init__(self):
        self.config = get_auth_config()

    def generate_access_token(self, user_id: UUID) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self.config.access_token_expire_minutes)
        to_encode = {
            "sub": str(user_id),
            "exp": expire,
            "type": "access"
        }
        encoded_jwt = jwt.encode(
            to_encode, 
            self.config.jwt_secret_key, 
            algorithm=self.config.jwt_algorithm
        )
        return encoded_jwt

    def generate_refresh_token(self, user_id: UUID) -> str:
        # Refresh tokens can be opaque strings since we store them in the DB.
        # Alternatively, they can be JWTs. Let's make them cryptographically random strings.
        return secrets.token_urlsafe(64)

    def verify_access_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(
                token, 
                self.config.jwt_secret_key, 
                algorithms=[self.config.jwt_algorithm]
            )
            if payload.get("type") != "access":
                raise InvalidTokenException("Not an access token.")
            return payload
        except jwt.ExpiredSignatureError:
            raise InvalidTokenException("Access token has expired.")
        except jwt.PyJWTError:
            raise InvalidTokenException("Could not validate credentials.")
