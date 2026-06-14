from typing import Optional
from app.modules.profile.application.queries.get_profile.get_profile_query import GetProfileQuery
from app.modules.profile.application.ports.output.profile_repository_port import ProfileRepositoryPort
from app.modules.profile.domain.entities.profile import Profile
from app.modules.profile.domain.exceptions.profile_exceptions import ProfileNotFoundException

class GetProfileHandler:
    def __init__(self, profile_repo: ProfileRepositoryPort):
        self.profile_repo = profile_repo

    def execute(self, query: GetProfileQuery) -> Profile:
        profile = self.profile_repo.get_by_auth_user_id(query.auth_user_id)
        if not profile:
            raise ProfileNotFoundException()
        return profile
