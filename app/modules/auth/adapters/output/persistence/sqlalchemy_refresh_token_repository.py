from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from app.modules.auth.application.ports.output.refresh_token_repository_port import RefreshTokenRepositoryPort
from app.modules.auth.domain.entities.refresh_token import RefreshToken
from app.modules.auth.adapters.output.persistence.models.refresh_token_model import RefreshTokenModel

class SqlAlchemyRefreshTokenRepository(RefreshTokenRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, model: RefreshTokenModel) -> RefreshToken:
        return RefreshToken(
            id=UUID(model.id) if isinstance(model.id, str) else model.id,
            token_string=model.token_string,
            user_id=UUID(model.user_id) if isinstance(model.user_id, str) else model.user_id,
            expires_at=model.expires_at,
            is_revoked=model.is_revoked,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def save(self, refresh_token: RefreshToken) -> None:
        db_token = RefreshTokenModel(
            id=refresh_token.id,
            token_string=refresh_token.token_string,
            user_id=refresh_token.user_id,
            expires_at=refresh_token.expires_at,
            is_revoked=refresh_token.is_revoked,
            created_at=refresh_token.created_at,
            updated_at=refresh_token.updated_at
        )
        self.session.merge(db_token)

    def get(self, id: UUID) -> Optional[RefreshToken]:
        db_token = self.session.query(RefreshTokenModel).filter(RefreshTokenModel.id == id).first()
        if db_token:
            return self._to_domain(db_token)
        return None

    def get_by_token(self, token_string: str) -> Optional[RefreshToken]:
        db_token = self.session.query(RefreshTokenModel).filter(RefreshTokenModel.token_string == token_string).first()
        if db_token:
            return self._to_domain(db_token)
        return None

    def delete(self, id: UUID) -> None:
        db_token = self.session.query(RefreshTokenModel).filter(RefreshTokenModel.id == id).first()
        if db_token:
            self.session.delete(db_token)

