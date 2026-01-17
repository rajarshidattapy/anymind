"""API Key management endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_active_user  # API keys require JWT auth
from app.models.user import User
from app.schemas.api_key import APIKeyCreate, APIKeyResponse, APIKeyCreateResponse
from app.services.api_key_service import APIKeyService

router = APIRouter()


@router.post("", response_model=APIKeyCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    key_data: APIKeyCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new API key."""
    api_key, plain_key = APIKeyService.create_api_key(db, current_user.id, key_data)
    return {
        "id": api_key.id,
        "key": plain_key,  # Only shown once
        "key_prefix": api_key.key_prefix,
        "name": api_key.name,
        "created_at": api_key.created_at
    }


@router.get("", response_model=List[APIKeyResponse])
async def list_api_keys(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List user's API keys."""
    return APIKeyService.list_api_keys(db, current_user.id)


@router.delete("/{api_key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(
    api_key_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Revoke an API key."""
    if not APIKeyService.revoke_api_key(db, api_key_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )

