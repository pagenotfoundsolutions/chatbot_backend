from app.shared.database.database import Base, engine

# Register tables by importing each FEATURE's models package (its __init__.py
# imports that feature's model classes). Tables register on Base.metadata BEFORE
# create_all() runs.
#   - New MODEL    -> add it to that feature's models/__init__.py (next to it).
#   - New FEATURE  -> add one import line here.
import app.modules.chat.adapters.output.persistence.models  # noqa: F401
import app.modules.auth.adapters.output.persistence.models  # noqa: F401
import app.modules.profile.adapters.output.persistence.models  # noqa: F401


def init_db() -> None:
    """Create all tables that are registered on Base.metadata."""
    # We no longer run Base.metadata.create_all(bind=engine) here.
    # Database schema management and migrations are now handled by Alembic.
    pass
