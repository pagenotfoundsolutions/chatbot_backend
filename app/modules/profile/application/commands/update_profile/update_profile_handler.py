from app.modules.profile.application.commands.update_profile.update_profile_command import UpdateProfileCommand
from app.modules.profile.application.ports.output.profile_repository_port import ProfileRepositoryPort
from app.modules.profile.domain.entities.profile import Profile
from app.modules.profile.domain.exceptions.profile_exceptions import ProfileNotFoundException

class UpdateProfileHandler:
    def __init__(self, profile_repo: ProfileRepositoryPort):
        self.profile_repo = profile_repo

    def execute(self, command: UpdateProfileCommand) -> Profile:
        profile = self.profile_repo.get(command.profile_id)
        if not profile:
            raise ProfileNotFoundException()

        profile.update(
            name=command.name,
            profile_image_url=command.profile_image_url,
            dob=command.dob
        )
        self.profile_repo.save(profile)
        return profile
