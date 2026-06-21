from uuid import UUID
from app.modules.profile.domain.entities.profile import Profile
from app.modules.profile.adapters.output.persistence.models.profile_model import ProfileModel

class ProfileMapper:
    @staticmethod
    def to_domain(model: ProfileModel) -> Profile:
        return Profile(
            id=model.id,
            auth_user_id=model.auth_user_id,
            name=model.name,
            profile_image_url=model.profile_image_url,
            dob=model.dob
        )

    @staticmethod
    def to_persistence(entity: Profile) -> ProfileModel:
        return ProfileModel(
            id=entity.id,
            auth_user_id=entity.auth_user_id,
            name=entity.name,
            profile_image_url=entity.profile_image_url,
            dob=entity.dob
        )
