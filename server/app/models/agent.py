"""Agent model."""
from sqlalchemy import Column, String, Text, ForeignKey, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.db.base import BaseModel


class AgentStatus(str, enum.Enum):
    """Agent status enumeration."""
    DRAFT = "draft"
    BUILDING = "building"
    READY = "ready"
    FAILED = "failed"
    ARCHIVED = "archived"


class Agent(BaseModel):
    """Agent model."""
    __tablename__ = "agents"
    
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SQLEnum(AgentStatus), default=AgentStatus.DRAFT, nullable=False)
    current_version_id = Column(Integer, ForeignKey("agent_versions.id"), nullable=True)
    
    user = relationship("User", backref="agents")
    versions = relationship("AgentVersion", back_populates="agent", foreign_keys="AgentVersion.agent_id")
    current_version = relationship("AgentVersion", foreign_keys=[current_version_id], post_update=True)

