from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.modules.profile.application.ports.output.profile_repository_port import ProfileRepositoryPort
from app.modules.profile.domain.entities.profile import Profile
from app.modules.profile.adapters.output.persistence.models.profile_model import ProfileModel
from app.modules.profile.adapters.output.persistence.profile_mapper import ProfileMapper

class SqlAlchemyProfileRepository(ProfileRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def save(self, profile: Profile) -> None:
        db_profile = ProfileMapper.to_persistence(profile)
        self.session.merge(db_profile)

    def get(self, id: UUID) -> Optional[Profile]:
        db_profile = self.session.query(ProfileModel).filter(ProfileModel.id == str(id)).first()
        if db_profile:
            return ProfileMapper.to_domain(db_profile)
        return None

    def get_by_auth_user_id(self, auth_user_id: UUID) -> Optional[Profile]:
        db_profile = self.session.query(ProfileModel).filter(ProfileModel.auth_user_id == str(auth_user_id)).first()
        if db_profile:
            return ProfileMapper.to_domain(db_profile)
        return None

    def delete(self, id: UUID) -> None:
        db_profile = self.session.query(ProfileModel).filter(ProfileModel.id == str(id)).first()
        if db_profile:
            self.session.delete(db_profile)
