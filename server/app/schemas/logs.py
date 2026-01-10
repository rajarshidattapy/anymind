"""Log schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LogEntry(BaseModel):
    """Log entry schema."""
    timestamp: datetime
    level: str
    message: str
    source: Optional[str] = None
    metadata: Optional[dict] = None


class LogQuery(BaseModel):
    """Log query schema."""
    execution_id: Optional[int] = None
    agent_version_id: Optional[int] = None
    level: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: int = 100

