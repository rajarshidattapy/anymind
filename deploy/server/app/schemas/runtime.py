"""Runtime execution schemas."""
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from app.models.execution import ExecutionStatus


class ExecutionCreate(BaseModel):
    """Execution creation schema."""
    agent_version_id: int
    input_data: Optional[dict[str, Any]] = None


class ExecutionResponse(BaseModel):
    """Execution response schema."""
    id: int
    agent_version_id: int
    user_id: int
    status: ExecutionStatus
    input_data: Optional[dict[str, Any]]
    output_data: Optional[dict[str, Any]]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ExecutionUpdate(BaseModel):
    """Execution update schema."""
    status: Optional[ExecutionStatus] = None
    output_data: Optional[dict[str, Any]] = None
    error_message: Optional[str] = None

