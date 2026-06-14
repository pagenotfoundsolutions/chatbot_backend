from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.shared.database.session import get_db
from app.modules.profile.adapters.output.persistence.sqlalchemy_profile_repository import SqlAlchemyProfileRepository
from app.modules.profile.application.commands.create_profile.create_profile_handler import CreateProfileHandler
from app.modules.profile.application.commands.update_profile.update_profile_handler import UpdateProfileHandler
from app.modules.profile.application.queries.get_profile.get_profile_handler import GetProfileHandler

def get_profile_repository(db_session: Annotated[Session, Depends(get_db)]) -> SqlAlchemyProfileRepository:
    return SqlAlchemyProfileRepository(session=db_session)

def get_create_profile_handler(
    repo: Annotated[SqlAlchemyProfileRepository, Depends(get_profile_repository)]
) -> CreateProfileHandler:
    return CreateProfileHandler(profile_repo=repo)

def get_update_profile_handler(
    repo: Annotated[SqlAlchemyProfileRepository, Depends(get_profile_repository)]
) -> UpdateProfileHandler:
    return UpdateProfileHandler(profile_repo=repo)

def get_get_profile_handler(
    repo: Annotated[SqlAlchemyProfileRepository, Depends(get_profile_repository)]
) -> GetProfileHandler:
    return GetProfileHandler(profile_repo=repo)
