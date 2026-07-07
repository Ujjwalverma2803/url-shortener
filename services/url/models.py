from sqlalchemy import (
    Column, String, Boolean,
    DateTime, Text, Integer
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    original_url = Column(Text, nullable=False)
    short_slug = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        nullable=True
    )
    custom_slug = Column(Boolean, default=False)
    click_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    expires_at = Column(
        DateTime(timezone=True),
        nullable=True
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )