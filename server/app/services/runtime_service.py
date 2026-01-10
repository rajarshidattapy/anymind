"""Runtime service for executing agents."""
import importlib.util
import sys
import tempfile
import logging
import signal
from typing import List, Optional, Any, Dict
from pathlib import Path
from sqlalchemy.orm import Session
from app.models.execution import Execution, ExecutionStatus
from app.models.agent_version import AgentVersion, VersionStatus
from app.models.agent import Agent
from app.schemas.runtime import ExecutionCreate, ExecutionUpdate
from app.core.config import settings
from app.utils.tarball import extract_tarball

logger = logging.getLogger(__name__)


class RuntimeService:
    """Service for runtime operations."""
    
    EXECUTION_TIMEOUT = 30  # seconds
    
    @staticmethod
    def get_latest_ready_version(db: Session, agent_id: int) -> Optional[AgentVersion]:
        """Get the latest ready version for an agent."""
        return db.query(AgentVersion).filter(
            AgentVersion.agent_id == agent_id,
            AgentVersion.status == VersionStatus.READY
        ).order_by(AgentVersion.id.desc()).first()
    
    @staticmethod
    def execute_agent(
        db: Session,
        agent_id: int,
        payload: Dict[str, Any],
        user_id: int
    ) -> Execution:
        """Execute an agent with the latest ready version."""
        # Get agent
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise ValueError("Agent not found")
        
        # Get latest ready version
        agent_version = RuntimeService.get_latest_ready_version(db, agent_id)
        if not agent_version:
            raise ValueError("No ready version available for this agent")
        
        if not agent_version.entrypoint:
            raise ValueError("Agent version has no entrypoint configured")
        
        # Create execution record
        execution = Execution(
            agent_version_id=agent_version.id,
            user_id=user_id,
            status=ExecutionStatus.RUNNING,
            input_data=payload
        )
        db.add(execution)
        db.commit()
        db.refresh(execution)
        
        # Execute agent with timeout
        try:
            import threading
            import queue
            
            # Use threading for timeout (cross-platform)
            result_queue = queue.Queue()
            exception_queue = queue.Queue()
            
            def run_agent():
                try:
                    output, logs = RuntimeService._run_agent(
                        agent_version,
                        payload,
                        execution.id
                    )
                    result_queue.put((output, logs))
                except Exception as e:
                    exception_queue.put(e)
            
            thread = threading.Thread(target=run_agent, daemon=True)
            thread.start()
            thread.join(timeout=RuntimeService.EXECUTION_TIMEOUT)
            
            if thread.is_alive():
                # Thread is still running, timeout occurred
                execution.status = ExecutionStatus.FAILED
                execution.error_message = "Execution timeout"
                execution.logs = f"Execution exceeded timeout limit of {RuntimeService.EXECUTION_TIMEOUT} seconds"
            elif not exception_queue.empty():
                # Exception occurred
                e = exception_queue.get()
                execution.status = ExecutionStatus.FAILED
                execution.error_message = str(e)
                execution.logs = f"Execution error: {str(e)}"
            else:
                # Success
                output, logs = result_queue.get()
                execution.status = ExecutionStatus.COMPLETED
                execution.output_data = output
                execution.logs = logs
                
        except Exception as e:
            execution.status = ExecutionStatus.FAILED
            execution.error_message = str(e)
            execution.logs = f"Execution error: {str(e)}"
        
        db.commit()
        db.refresh(execution)
        return execution
    
    @staticmethod
    def _run_agent(
        agent_version: AgentVersion,
        payload: Dict[str, Any],
        execution_id: int
    ) -> tuple[Dict[str, Any], str]:
        """Run the agent and return output and logs."""
        tarball_path = Path(settings.STORAGE_PATH) / agent_version.tarball_path
        
        if not tarball_path.exists():
            raise FileNotFoundError(f"Tarball not found: {agent_version.tarball_path}")
        
        # Extract to temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            extract_path = Path(temp_dir) / "agent"
            
            if not extract_tarball(tarball_path, extract_path):
                raise RuntimeError("Failed to extract agent tarball")
            
            # Parse entrypoint
            module_path, function_name = agent_version.entrypoint.split(":", 1)
            
            # Find module file
            module_file = None
            for py_file in extract_path.rglob("*.py"):
                relative_path = py_file.relative_to(extract_path)
                module_parts = str(relative_path.with_suffix("")).replace("/", ".").replace("\\", ".")
                
                if module_parts == module_path or module_parts.endswith(f".{module_path}"):
                    module_file = py_file
                    break
            
            if not module_file:
                raise ImportError(f"Module '{module_path}' not found")
            
            # Add extract path to sys.path temporarily
            sys.path.insert(0, str(extract_path))
            
            try:
                # Import module
                spec = importlib.util.spec_from_file_location(module_path, module_file)
                if spec is None or spec.loader is None:
                    raise ImportError(f"Failed to load module '{module_path}'")
                
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Get function
                if not hasattr(module, function_name):
                    raise AttributeError(f"Function '{function_name}' not found")
                
                handler = getattr(module, function_name)
                
                # Execute handler (timeout handled at application level for cross-platform)
                # For production, consider using threading.Timer or asyncio timeout
                try:
                    # Call handler
                    result = handler(payload)
                    
                    # Ensure result is serializable
                    if not isinstance(result, dict):
                        result = {"result": result}
                    
                    return result, f"Execution {execution_id} completed successfully"
                    
                except Exception as e:
                    raise
                    
            finally:
                # Remove from sys.path
                if str(extract_path) in sys.path:
                    sys.path.remove(str(extract_path))
    
    @staticmethod
    def create_execution(
        db: Session,
        execution_data: ExecutionCreate,
        user_id: int
    ) -> Execution:
        """Create a new execution."""
        execution = Execution(
            agent_version_id=execution_data.agent_version_id,
            user_id=user_id,
            status=ExecutionStatus.PENDING,
            input_data=execution_data.input_data
        )
        db.add(execution)
        db.commit()
        db.refresh(execution)
        return execution
    
    @staticmethod
    def get_execution(db: Session, execution_id: int, user_id: int) -> Optional[Execution]:
        """Get an execution by ID."""
        return db.query(Execution).filter(
            Execution.id == execution_id,
            Execution.user_id == user_id
        ).first()
    
    @staticmethod
    def list_executions(
        db: Session,
        user_id: int,
        agent_version_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Execution]:
        """List executions."""
        query = db.query(Execution).filter(Execution.user_id == user_id)
        
        if agent_version_id:
            query = query.filter(Execution.agent_version_id == agent_version_id)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_execution(
        db: Session,
        execution_id: int,
        user_id: int,
        execution_data: ExecutionUpdate
    ) -> Optional[Execution]:
        """Update an execution."""
        execution = RuntimeService.get_execution(db, execution_id, user_id)
        if not execution:
            return None
        
        update_data = execution_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(execution, field, value)
        
        db.commit()
        db.refresh(execution)
        return execution
    
    @staticmethod
    def cancel_execution(db: Session, execution_id: int, user_id: int) -> Optional[Execution]:
        """Cancel an execution."""
        execution = RuntimeService.get_execution(db, execution_id, user_id)
        if not execution:
            return None
        
        if execution.status in [ExecutionStatus.PENDING, ExecutionStatus.RUNNING]:
            execution.status = ExecutionStatus.CANCELLED
            db.commit()
            db.refresh(execution)
        
        return execution

