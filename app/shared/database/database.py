from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session, with_loader_criteria, ORMExecuteState
from sqlalchemy.orm import declarative_base

from app.shared.config.settings import settings


DATABASE_URL = settings.database_url

engine=create_engine(
    DATABASE_URL,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base=declarative_base()

@event.listens_for(Session, "do_orm_execute")
def _add_soft_delete_criteria(execute_state: ORMExecuteState) -> None:
    """Automatically append `deleted_at IS NULL` to all queries on tables that have this column."""
    if execute_state.execution_options.get("include_deleted", False):
        return

    if execute_state.is_select and not execute_state.is_column_load and not execute_state.is_relationship_load:
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                Base,
                lambda cls: cls.deleted_at.is_(None) if hasattr(cls, "deleted_at") else None,
                include_aliases=True,
            )
        )