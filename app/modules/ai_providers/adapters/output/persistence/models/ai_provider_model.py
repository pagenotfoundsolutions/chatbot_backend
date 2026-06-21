from sqlalchemy import Column, String, Boolean, DateTime, Float, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.shared.database.database import Base
from app.shared.database.core_model import CoreModelMixin

class AIProviderModel(CoreModelMixin, Base):
    __tablename__ = "ai_providers"

    name = Column(String(50), nullable=False, unique=True, index=True)
    display_name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    api_base_url = Column(String(255), nullable=False)
    api_key = Column(String(255), nullable=False)

    models = relationship("AIModelModel", back_populates="provider", cascade="all, delete-orphan")
