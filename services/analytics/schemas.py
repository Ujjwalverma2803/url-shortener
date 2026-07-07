from pydantic import BaseModel

class ClickEvent(BaseModel):
    slug: str
    ip: str
    user_agent: str
    referrer: str = ""