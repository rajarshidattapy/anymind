"""Authentication schemas."""
from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema."""
    user_id: Optional[int] = None


class UserLogin(BaseModel):
    """User login schema."""
    username: str
    password: str


class UserRegister(BaseModel):
    """User registration schema."""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    
    class Config:
        from_attributes = True

