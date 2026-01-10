"""Agent service."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.agent import Agent, AgentStatus
from app.models.agent_version import AgentVersion
from app.schemas.agent import AgentCreate, AgentUpdate


class AgentService:
    """Service for agent operations."""
    
    @staticmethod
    def create_agent(db: Session, agent_data: AgentCreate, user_id: int) -> Agent:
        """Create a new agent."""
        agent = Agent(
            name=agent_data.name,
            description=agent_data.description,
            user_id=user_id,
            status=AgentStatus.DRAFT
        )
        db.add(agent)
        db.commit()
        db.refresh(agent)
        return agent
    
    @staticmethod
    def get_agent(db: Session, agent_id: int, user_id: int) -> Optional[Agent]:
        """Get an agent by ID."""
        return db.query(Agent).filter(
            Agent.id == agent_id,
            Agent.user_id == user_id
        ).first()
    
    @staticmethod
    def list_agents(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Agent]:
        """List user's agents."""
        return db.query(Agent).filter(
            Agent.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_agent(
        db: Session,
        agent_id: int,
        user_id: int,
        agent_data: AgentUpdate
    ) -> Optional[Agent]:
        """Update an agent."""
        agent = AgentService.get_agent(db, agent_id, user_id)
        if not agent:
            return None
        
        update_data = agent_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(agent, field, value)
        
        db.commit()
        db.refresh(agent)
        return agent
    
    @staticmethod
    def delete_agent(db: Session, agent_id: int, user_id: int) -> bool:
        """Delete an agent."""
        agent = AgentService.get_agent(db, agent_id, user_id)
        if not agent:
            return False
        
        db.delete(agent)
        db.commit()
        return True

