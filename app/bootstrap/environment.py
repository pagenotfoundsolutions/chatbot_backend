from __future__ import annotations

from app.shared.config.settings import Settings, get_settings

# The bootstrap layer's view of the environment. Today it simply re-exposes the
# shared Settings singleton; centralising it here means future env concerns
# (profiles, feature flags, secret loading) have one obvious home.

__all__ = ["Settings", "get_settings"]
