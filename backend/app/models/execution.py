"""Execution model."""
from sqlalchemy import Column, String, Text, ForeignKey, Integer, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
import enum
from app.db.base import BaseModel


class ExecutionStatus(str, enum.Enum):
    """Execution status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Execution(BaseModel):
    """Execution model."""
    __tablename__ = "executions"
    
    agent_version_id = Column(Integer, ForeignKey("agent_versions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SQLEnum(ExecutionStatus), default=ExecutionStatus.PENDING, nullable=False)
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    logs = Column(Text, nullable=True)
    
    agent_version = relationship("AgentVersion", back_populates="executions")
    user = relationship("User", backref="executions")

