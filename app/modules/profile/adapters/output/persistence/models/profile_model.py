from datetime import date, datetime
from sqlalchemy import String, Date, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.shared.database.database import Base

class ProfileModel(Base):
    __tablename__ = "profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    auth_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("auth_users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    profile_image_url: Mapped[str] = mapped_column(String(1024), nullable=True)
    dob: Mapped[date] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
