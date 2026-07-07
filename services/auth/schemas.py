from pydantic import BaseModel, EmailStr
from enum import Enum
import uuid

class UserTier(str, Enum):
    FREE = "free"
    PREMIUM = "premium"

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    tier: UserTier
    is_active: bool

    class Config:
        from_attributes = True