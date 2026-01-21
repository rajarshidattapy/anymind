"""API Key schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class APIKeyCreate(BaseModel):
    """API Key creation schema."""
    name: str


class APIKeyResponse(BaseModel):
    """API Key response schema."""
    id: int
    key_prefix: str
    name: str
    is_active: bool
    last_used_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class APIKeyCreateResponse(BaseModel):
    """API Key creation response with full key (only shown once)."""
    id: int
    key: str  # Full key, only shown on creation
    key_prefix: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

