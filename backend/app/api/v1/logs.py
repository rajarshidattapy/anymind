"""Log endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_authenticated_user
from app.models.user import User
from app.models.execution import Execution
from app.models.agent_version import AgentVersion
from app.models.agent import Agent
from app.schemas.logs import LogQuery, LogEntry
from datetime import datetime

router = APIRouter()


@router.get("/{agent_id}", response_model=List[LogEntry])
async def get_agent_logs(
    agent_id: int,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    """Get logs for an agent (build logs and execution logs)."""
    # Verify agent belongs to user
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.user_id == current_user.id
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    logs = []
    
    # Get build logs from versions
    versions = db.query(AgentVersion).filter(
        AgentVersion.agent_id == agent_id
    ).order_by(AgentVersion.created_at.desc()).limit(10).all()
    
    for version in versions:
        if version.build_log:
            logs.append(LogEntry(
                timestamp=version.created_at,
                level="INFO" if version.status.value == "ready" else "ERROR",
                message=f"Build {version.version}: {version.build_log}",
                source="build",
                metadata={"version_id": version.id, "status": version.status.value}
            ))
    
    # Get execution logs
    executions = db.query(Execution).join(AgentVersion).filter(
        AgentVersion.agent_id == agent_id,
        Execution.user_id == current_user.id
    ).order_by(Execution.created_at.desc()).limit(50).all()
    
    for execution in executions:
        if execution.logs:
            logs.append(LogEntry(
                timestamp=execution.created_at,
                level="INFO" if execution.status.value == "completed" else "ERROR",
                message=execution.logs,
                source="runtime",
                metadata={
                    "execution_id": execution.id,
                    "status": execution.status.value
                }
            ))
        if execution.error_message:
            logs.append(LogEntry(
                timestamp=execution.updated_at or execution.created_at,
                level="ERROR",
                message=execution.error_message,
                source="runtime",
                metadata={
                    "execution_id": execution.id,
                    "status": execution.status.value
                }
            ))
    
    # Sort by timestamp
    logs.sort(key=lambda x: x.timestamp, reverse=True)
    
    return logs[:100]  # Limit to 100 most recent


@router.get("/executions/{execution_id}/logs", response_model=List[LogEntry])
async def get_execution_logs(
    execution_id: int,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    """Get logs for a specific execution."""
    execution = db.query(Execution).filter(
        Execution.id == execution_id,
        Execution.user_id == current_user.id
    ).first()
    
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found"
        )
    
    logs = []
    
    if execution.logs:
        logs.append(LogEntry(
            timestamp=execution.created_at,
            level="INFO",
            message=execution.logs,
            source="runtime",
            metadata={"execution_id": execution.id}
        ))
    
    if execution.error_message:
        logs.append(LogEntry(
            timestamp=execution.updated_at or execution.created_at,
            level="ERROR",
            message=execution.error_message,
            source="runtime",
            metadata={"execution_id": execution.id}
        ))
    
    return logs

