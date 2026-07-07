from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
import uuid

class URLCreate(BaseModel):
    original_url: HttpUrl
    custom_slug: Optional[str] = None
    expires_at: Optional[datetime] = None

class URLResponse(BaseModel):
    id: uuid.UUID
    original_url: str
    short_slug: str
    short_url: str
    click_count: int
    expires_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True