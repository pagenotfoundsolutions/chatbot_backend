import uuid
from datetime import datetime, timezone

def generate_uuid() -> str:
    """Generate a new UUIDv4 string."""
    return str(uuid.uuid4())

def utc_now() -> datetime:
    """Get the current datetime in UTC timezone."""
    return datetime.now(timezone.utc)
