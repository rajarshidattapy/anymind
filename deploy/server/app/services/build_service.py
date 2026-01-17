"""Build service for agent versions."""
import json
import yaml
import importlib.util
import sys
from typing import Optional
from sqlalchemy.orm import Session
from pathlib import Path
from app.models.agent_version import AgentVersion, VersionStatus
from app.models.agent import Agent
from app.core.config import settings
from app.utils.tarball import extract_tarball, validate_tarball


class BuildService:
    """Service for building agent versions."""
    
    @staticmethod
    def create_version_from_upload(
        db: Session,
        agent_id: int,
        tarball_path: str
    ) -> Optional[AgentVersion]:
        """Create a new agent version from uploaded tarball."""
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            return None
        
        # Generate version number (simple increment)
        existing_versions = db.query(AgentVersion).filter(
            AgentVersion.agent_id == agent_id
        ).order_by(AgentVersion.id.desc()).all()
        
        version_number = f"v{len(existing_versions) + 1}"
        
        # Create agent version with QUEUED status
        agent_version = AgentVersion(
            agent_id=agent_id,
            version=version_number,
            status=VersionStatus.QUEUED,
            tarball_path=tarball_path
        )
        db.add(agent_version)
        db.commit()
        db.refresh(agent_version)
        
        return agent_version
    
    @staticmethod
    def get_build(db: Session, build_id: int) -> Optional[AgentVersion]:
        """Get a build by ID."""
        return db.query(AgentVersion).filter(AgentVersion.id == build_id).first()
    
    @staticmethod
    def update_build_status(
        db: Session,
        build_id: int,
        status: VersionStatus,
        build_log: Optional[str] = None,
        entrypoint: Optional[str] = None
    ) -> Optional[AgentVersion]:
        """Update build status."""
        build = BuildService.get_build(db, build_id)
        if not build:
            return None
        
        build.status = status
        if build_log:
            build.build_log = build_log
        if entrypoint:
            build.entrypoint = entrypoint
        
        db.commit()
        db.refresh(build)
        return build
    
    @staticmethod
    def validate_agent_artifact(tarball_path: Path, extract_dir: Path) -> tuple[bool, Optional[str], Optional[str]]:
        """
        Validate agent artifact.
        Returns: (is_valid, error_message, entrypoint)
        """
        try:
            # Extract tarball
            if not extract_tarball(tarball_path, extract_dir):
                return False, "Failed to extract tarball", None
            
            # Find anymind.yaml
            yaml_files = list(extract_dir.rglob("anymind.yaml"))
            if not yaml_files:
                return False, "anymind.yaml not found in artifact", None
            
            yaml_path = yaml_files[0]
            
            # Parse anymind.yaml
            try:
                with open(yaml_path, 'r') as f:
                    config = yaml.safe_load(f)
            except Exception as e:
                return False, f"Failed to parse anymind.yaml: {str(e)}", None
            
            # Validate required fields
            if not isinstance(config, dict):
                return False, "anymind.yaml must be a YAML object", None
            
            if "entrypoint" not in config:
                return False, "entrypoint not found in anymind.yaml", None
            
            entrypoint = config["entrypoint"]
            if not isinstance(entrypoint, str):
                return False, "entrypoint must be a string", None
            
            # Validate entrypoint format (module:function)
            if ":" not in entrypoint:
                return False, "entrypoint must be in format 'module:function'", None
            
            module_path, function_name = entrypoint.split(":", 1)
            
            # Try to find and import the module
            module_file = None
            for py_file in extract_dir.rglob("*.py"):
                # Check if this file matches the module path
                relative_path = py_file.relative_to(extract_dir)
                module_parts = str(relative_path.with_suffix("")).replace("/", ".").replace("\\", ".")
                
                if module_parts == module_path or module_parts.endswith(f".{module_path}"):
                    module_file = py_file
                    break
            
            if not module_file:
                return False, f"Module '{module_path}' not found in artifact", None
            
            # Try to import and validate the function exists
            try:
                spec = importlib.util.spec_from_file_location(module_path, module_file)
                if spec is None or spec.loader is None:
                    return False, f"Failed to load module '{module_path}'", None
                
                module = importlib.util.module_from_spec(spec)
                sys.modules[f"_temp_{module_path}"] = module
                spec.loader.exec_module(module)
                
                if not hasattr(module, function_name):
                    return False, f"Function '{function_name}' not found in module '{module_path}'", None
                
                func = getattr(module, function_name)
                if not callable(func):
                    return False, f"'{function_name}' is not callable", None
                
                # Clean up
                del sys.modules[f"_temp_{module_path}"]
                
            except Exception as e:
                return False, f"Failed to validate entrypoint: {str(e)}", None
            
            return True, None, entrypoint
            
        except Exception as e:
            return False, f"Validation error: {str(e)}", None

