import uuid
from datetime import datetime, timezone

def generate_uuid() -> uuid.UUID:
    """Generate a new UUIDv4."""
    return uuid.uuid4()

def utc_now() -> datetime:
    """Get the current datetime in UTC timezone."""
    return datetime.now(timezone.utc)
