from app.modules.profile.application.commands.create_profile.create_profile_command import CreateProfileCommand
from app.modules.profile.application.ports.output.profile_repository_port import ProfileRepositoryPort
from app.modules.profile.domain.entities.profile import Profile

class CreateProfileHandler:
    def __init__(self, profile_repo: ProfileRepositoryPort):
        self.profile_repo = profile_repo

    def execute(self, command: CreateProfileCommand) -> Profile:
        existing_profile = self.profile_repo.get_by_auth_user_id(command.auth_user_id)
        if existing_profile:
            # For simplicity, returning existing profile instead of error
            return existing_profile

        profile = Profile.create(
            auth_user_id=command.auth_user_id,
            name=command.name,
            profile_image_url=command.profile_image_url,
            dob=command.dob
        )
        self.profile_repo.save(profile)
        return profile
