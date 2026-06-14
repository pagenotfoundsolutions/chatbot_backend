from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from app.modules.auth.application.ports.output.auth_user_repository_port import AuthUserRepositoryPort
from app.modules.auth.domain.entities.auth_user import AuthUser
from app.modules.auth.adapters.output.persistence.models.auth_user_model import AuthUserModel
from app.modules.auth.adapters.output.persistence.auth_user_mapper import AuthUserMapper

class SqlAlchemyAuthUserRepository(AuthUserRepositoryPort):
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, user: AuthUser) -> None:
        db_user = AuthUserMapper.to_persistence(user)
        self.session.merge(db_user) # merge handles insert and update
    
    def get(self, id: UUID) -> Optional[AuthUser]:
        db_user = self.session.query(AuthUserModel).filter(AuthUserModel.id == str(id)).first()
        if db_user:
            return AuthUserMapper.to_domain(db_user)
        return None
        
    def delete(self, id: UUID) -> None:
        db_user = self.session.query(AuthUserModel).filter(AuthUserModel.id == str(id)).first()
        if db_user:
            self.session.delete(db_user)

    def get_by_email(self, email: str) -> Optional[AuthUser]:
        db_user = self.session.query(AuthUserModel).filter(AuthUserModel.email == email).first()
        if db_user:
            return AuthUserMapper.to_domain(db_user)
        return None