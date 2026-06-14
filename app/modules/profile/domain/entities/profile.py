from datetime import date
from typing import Optional
from uuid import UUID

from app.shared.kernel.aggregate_root import AggregateRoot


class Profile(AggregateRoot[UUID]):
    def __init__(
        self,
        id: UUID,
        auth_user_id: UUID,
        name: str,
        profile_image_url: Optional[str] = None,
        dob: Optional[date] = None
    ) -> None:
        super().__init__(id)
        self.auth_user_id = auth_user_id
        self.name = name
        self.profile_image_url = profile_image_url
        self.dob = dob

    @classmethod
    def create(
        cls,
        auth_user_id: UUID,
        name: str,
        profile_image_url: Optional[str] = None,
        dob: Optional[date] = None
    ) -> 'Profile':
        from uuid import uuid4
        return cls(
            id=uuid4(),
            auth_user_id=auth_user_id,
            name=name,
            profile_image_url=profile_image_url,
            dob=dob
        )

    def update(
        self,
        name: str,
        profile_image_url: Optional[str] = None,
        dob: Optional[date] = None
    ) -> None:
        self.name = name
        self.profile_image_url = profile_image_url
        self.dob = dob
