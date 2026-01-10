"""File upload endpoints."""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from pathlib import Path
from app.core.dependencies import get_db, get_authenticated_user
from app.core.config import settings
from app.models.user import User
from app.services.storage_service import StorageService
from app.services.build_service import BuildService
from app.services.agent_service import AgentService
from app.workers.build_worker import BuildWorker
from app.schemas.agent import AgentVersionResponse

router = APIRouter()
storage_service = StorageService()


@router.post("/agent/{agent_id}", response_model=AgentVersionResponse, status_code=status.HTTP_201_CREATED)
async def upload_agent_artifact(
    agent_id: int,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    """Upload agent artifact (.tar.gz) and create a new version."""
    # Verify agent exists and belongs to user
    agent = AgentService.get_agent(db, agent_id, current_user.id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Validate file extension
    if not file.filename.endswith('.tar.gz'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a .tar.gz archive"
        )
    
    # Check file size
    contents = await file.read()
    if len(contents) > settings.UPLOAD_MAX_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum of {settings.UPLOAD_MAX_SIZE} bytes"
        )
    
    # Save tarball
    tarball_filename = f"agent_{agent_id}_{file.filename}"
    file_path = storage_service.save_file(
        contents,
        tarball_filename,
        f"agents/{agent_id}/artifacts"
    )
    
    if not file_path:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save file"
        )
    
    # Create agent version
    relative_path = str(file_path.relative_to(Path(settings.STORAGE_PATH)))
    agent_version = BuildService.create_version_from_upload(
        db,
        agent_id,
        relative_path
    )
    
    if not agent_version:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create agent version"
        )
    
    # Queue build job
    def process_build_task(build_id: int):
        """Background task wrapper for build processing."""
        worker = BuildWorker()
        worker.process_build(build_id)
    
    background_tasks.add_task(process_build_task, agent_version.id)
    
    return agent_version


@router.get("/{filepath:path}")
async def download_file(
    filepath: str,
    current_user: User = Depends(get_authenticated_user)
):
    """Download a file."""
    from fastapi.responses import Response
    
    file_content = storage_service.get_file(filepath)
    if not file_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    return Response(content=file_content, media_type="application/octet-stream")

