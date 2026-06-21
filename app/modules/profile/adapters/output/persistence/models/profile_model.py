import uuid
from sqlalchemy import Uuid
from datetime import date
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.shared.database.database import Base
from app.shared.database.core_model import CoreModelMixin

class ProfileModel(CoreModelMixin, Base):
    __tablename__ = "profiles"

    auth_user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("auth_users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    profile_image_url: Mapped[str] = mapped_column(String(1024), nullable=True)
    dob: Mapped[date] = mapped_column(Date, nullable=True)
