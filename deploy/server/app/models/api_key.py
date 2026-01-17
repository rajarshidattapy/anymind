"""API Key model."""
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import BaseModel


class APIKey(BaseModel):
    """API Key model."""
    __tablename__ = "api_keys"
    
    key_hash = Column(String, unique=True, index=True, nullable=False)  # Hashed API key
    key_prefix = Column(String, nullable=False)  # First 8 chars for display
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime, nullable=True)
    
    user = relationship("User", backref="api_keys")

