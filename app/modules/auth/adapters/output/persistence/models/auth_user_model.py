from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.shared.database.database import Base
from app.shared.database.core_model import CoreModelMixin

class AuthUserModel(CoreModelMixin, Base):
    __tablename__ = "auth_users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
