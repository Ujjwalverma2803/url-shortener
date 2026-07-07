from sqlalchemy import (
    Column, String,
    DateTime, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Click(Base):
    __tablename__ = "clicks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    slug = Column(
        String,
        nullable=False,
        index=True
    )
    ip_address = Column(String, nullable=True)
    country = Column(String, nullable=True)
    device_type = Column(String, nullable=True)
    browser = Column(String, nullable=True)
    referrer = Column(Text, nullable=True)
    clicked_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )