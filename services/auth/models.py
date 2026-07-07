from sqlalchemy import (
    Column, String, Boolean,
    DateTime, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid
import enum

Base = declarative_base()

class UserTier(str, enum.Enum):
    FREE = "free"
    PREMIUM = "premium"

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )
    hashed_password = Column(
        String,
        nullable=False
    )
    tier = Column(
        SAEnum(UserTier),
        default=UserTier.FREE,
        nullable=False
    )
    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )