"""Agent endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_authenticated_user
from app.models.user import User
from app.schemas.agent import AgentCreate, AgentUpdate, AgentResponse, AgentVersionCreate, AgentVersionResponse
from app.services.agent_service import AgentService

router = APIRouter()


@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    """Create a new agent."""
    return AgentService.create_agent(db, agent_data, current_user.id)


@router.get("", response_model=List[AgentResponse])
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    """List user's agents."""
    return AgentService.list_agents(db, current_user.id, skip, limit)


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: int,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    """Get an agent by ID."""
    agent = AgentService.get_agent(db, agent_id, current_user.id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return agent


@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    """Update an agent."""
    agent = AgentService.update_agent(db, agent_id, current_user.id, agent_data)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: int,
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    """Delete an agent."""
    if not AgentService.delete_agent(db, agent_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )

