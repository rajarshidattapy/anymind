"""Runtime execution endpoints."""
from typing import List, Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_authenticated_user
from app.models.user import User
from app.schemas.runtime import ExecutionCreate, ExecutionResponse, ExecutionUpdate
from app.services.runtime_service import RuntimeService
from pydantic import BaseModel

router = APIRouter()


class ExecuteRequest(BaseModel):
    """Execute request schema."""
    payload: Dict[str, Any]


@router.post("/{agent_id}/execute", response_model=ExecutionResponse, status_code=status.HTTP_201_CREATED)
async def execute_agent(
    agent_id: int,
    request: ExecuteRequest,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    """Execute an agent with the latest ready version."""
    try:
        execution = RuntimeService.execute_agent(
            db,
            agent_id,
            request.payload,
            current_user.id
        )
        return execution
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Execution failed: {str(e)}"
        )


@router.post("/execute", response_model=ExecutionResponse, status_code=status.HTTP_201_CREATED)
async def create_execution(
    execution_data: ExecutionCreate,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    """Create a new execution (legacy endpoint)."""
    return RuntimeService.create_execution(db, execution_data, current_user.id)


@router.get("/executions", response_model=List[ExecutionResponse])
async def list_executions(
    agent_version_id: int = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    """List executions."""
    return RuntimeService.list_executions(
        db,
        current_user.id,
        agent_version_id,
        skip,
        limit
    )


@router.get("/executions/{execution_id}", response_model=ExecutionResponse)
async def get_execution(
    execution_id: int,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    """Get an execution by ID."""
    execution = RuntimeService.get_execution(db, execution_id, current_user.id)
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found"
        )
    return execution


@router.patch("/executions/{execution_id}", response_model=ExecutionResponse)
async def update_execution(
    execution_id: int,
    execution_data: ExecutionUpdate,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    """Update an execution."""
    execution = RuntimeService.update_execution(
        db,
        execution_id,
        current_user.id,
        execution_data
    )
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found"
        )
    return execution


@router.post("/executions/{execution_id}/cancel", response_model=ExecutionResponse)
async def cancel_execution(
    execution_id: int,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    """Cancel an execution."""
    execution = RuntimeService.cancel_execution(db, execution_id, current_user.id)
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found"
        )
    return execution

