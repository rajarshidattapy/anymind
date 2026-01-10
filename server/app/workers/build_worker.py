"""Build worker for processing agent builds."""
import logging
import tempfile
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.agent_version import AgentVersion, VersionStatus
from app.services.build_service import BuildService
from app.core.config import settings

logger = logging.getLogger(__name__)


class BuildWorker:
    """Worker for processing agent builds."""
    
    def __init__(self):
        self.db: Session = SessionLocal()
    
    def process_build(self, build_id: int) -> bool:
        """Process a build job."""
        try:
            build = BuildService.get_build(self.db, build_id)
            if not build:
                logger.error(f"Build {build_id} not found")
                return False
            
            if build.status != VersionStatus.QUEUED:
                logger.warning(f"Build {build_id} is not in queued status")
                return False
            
            # Update status to BUILDING
            BuildService.update_build_status(
                self.db,
                build_id,
                VersionStatus.BUILDING,
                "Starting build validation..."
            )
            
            tarball_path = Path(settings.STORAGE_PATH) / build.tarball_path
            if not tarball_path.exists():
                BuildService.update_build_status(
                    self.db,
                    build_id,
                    VersionStatus.FAILED,
                    f"Tarball not found: {build.tarball_path}"
                )
                return False
            
            # Create temporary directory for extraction
            with tempfile.TemporaryDirectory() as temp_dir:
                extract_path = Path(temp_dir) / "extracted"
                
                # Validate artifact
                is_valid, error_msg, entrypoint = BuildService.validate_agent_artifact(
                    tarball_path,
                    extract_path
                )
                
                if not is_valid:
                    BuildService.update_build_status(
                        self.db,
                        build_id,
                        VersionStatus.FAILED,
                        error_msg or "Validation failed"
                    )
                    return False
                
                # Store config if available
                config_path = extract_path / "anymind.yaml"
                if config_path.exists():
                    import yaml
                    with open(config_path, 'r') as f:
                        config_data = yaml.safe_load(f)
                    build.config = yaml.dump(config_data)
                    self.db.commit()
                
                # Mark as ready
                BuildService.update_build_status(
                    self.db,
                    build_id,
                    VersionStatus.READY,
                    "Build completed successfully",
                    entrypoint
                )
                
                logger.info(f"Build {build_id} completed successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error processing build {build_id}: {e}", exc_info=True)
            BuildService.update_build_status(
                self.db,
                build_id,
                VersionStatus.FAILED,
                f"Build failed: {str(e)}"
            )
            return False
        finally:
            self.db.close()
    
    def __del__(self):
        """Cleanup."""
        if hasattr(self, 'db'):
            self.db.close()
