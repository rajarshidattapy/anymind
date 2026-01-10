"""Agent schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.agent import AgentStatus
from app.models.agent_version import VersionStatus


class AgentBase(BaseModel):
    """Base agent schema."""
    name: str
    description: Optional[str] = None


class AgentCreate(AgentBase):
    """Agent creation schema."""
    pass


class AgentUpdate(BaseModel):
    """Agent update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[AgentStatus] = None


class AgentResponse(AgentBase):
    """Agent response schema."""
    id: int
    user_id: int
    status: AgentStatus
    current_version_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AgentVersionBase(BaseModel):
    """Base agent version schema."""
    version: str
    config: Optional[str] = None


class AgentVersionCreate(AgentVersionBase):
    """Agent version creation schema."""
    agent_id: int


class AgentVersionResponse(AgentVersionBase):
    """Agent version response schema."""
    id: int
    agent_id: int
    status: VersionStatus
    build_log: Optional[str]
    tarball_path: Optional[str]
    entrypoint: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

