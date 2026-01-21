"""Usage tracking service."""
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.execution import Execution
from app.models.agent import Agent


class UsageService:
    """Service for tracking usage statistics."""
    
    @staticmethod
    def get_user_execution_count(
        db: Session,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> int:
        """Get execution count for a user."""
        query = db.query(Execution).filter(Execution.user_id == user_id)
        
        if start_date:
            query = query.filter(Execution.created_at >= start_date)
        if end_date:
            query = query.filter(Execution.created_at <= end_date)
        
        return query.count()
    
    @staticmethod
    def get_user_agent_count(db: Session, user_id: int) -> int:
        """Get agent count for a user."""
        return db.query(Agent).filter(Agent.user_id == user_id).count()
    
    @staticmethod
    def get_daily_usage(
        db: Session,
        user_id: int,
        days: int = 30
    ) -> dict:
        """Get daily usage statistics."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        executions = db.query(Execution).filter(
            Execution.user_id == user_id,
            Execution.created_at >= start_date,
            Execution.created_at <= end_date
        ).all()
        
        daily_counts = {}
        for execution in executions:
            date_key = execution.created_at.date().isoformat()
            daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
        
        return daily_counts

