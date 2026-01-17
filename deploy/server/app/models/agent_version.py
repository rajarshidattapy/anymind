"""Agent Version model."""
from sqlalchemy import Column, String, Text, ForeignKey, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.db.base import BaseModel


class VersionStatus(str, enum.Enum):
    """Version status enumeration."""
    QUEUED = "queued"
    BUILDING = "building"
    READY = "ready"
    FAILED = "failed"


class AgentVersion(BaseModel):
    """Agent Version model."""
    __tablename__ = "agent_versions"
    
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    version = Column(String, nullable=False)
    status = Column(SQLEnum(VersionStatus), default=VersionStatus.QUEUED, nullable=False)
    build_log = Column(Text, nullable=True)
    tarball_path = Column(String, nullable=True)
    config = Column(Text, nullable=True)  # JSON string
    entrypoint = Column(String, nullable=True)  # e.g., "agent.main:handle"
    
    agent = relationship("Agent", back_populates="versions", foreign_keys=[agent_id])
    executions = relationship("Execution", back_populates="agent_version")

