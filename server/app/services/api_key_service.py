"""API Key service."""
import secrets
import hashlib
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.api_key import APIKey
from app.core.security import get_password_hash, verify_password
from app.schemas.api_key import APIKeyCreate


class APIKeyService:
    """Service for API key operations."""
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate a new API key."""
        # Generate a secure random key
        return f"anymind_{secrets.token_urlsafe(32)}"
    
    @staticmethod
    def _hash_key(key: str) -> str:
        """Hash an API key using SHA256."""
        return hashlib.sha256(key.encode()).hexdigest()
    
    @staticmethod
    def create_api_key(
        db: Session,
        user_id: int,
        key_data: APIKeyCreate
    ) -> tuple[APIKey, str]:
        """Create a new API key and return it with the plain key (only shown once)."""
        # Generate key
        plain_key = APIKeyService.generate_api_key()
        key_hash = APIKeyService._hash_key(plain_key)
        key_prefix = plain_key[:12]  # First 12 chars for display
        
        # Create API key record
        api_key = APIKey(
            key_hash=key_hash,
            key_prefix=key_prefix,
            name=key_data.name,
            user_id=user_id,
            is_active=True
        )
        db.add(api_key)
        db.commit()
        db.refresh(api_key)
        
        return api_key, plain_key
    
    @staticmethod
    def verify_api_key(db: Session, api_key: str) -> Optional[APIKey]:
        """Verify an API key and return the APIKey object if valid."""
        # Hash the provided key
        provided_hash = APIKeyService._hash_key(api_key)
        
        # Get all active API keys
        api_keys = db.query(APIKey).filter(APIKey.is_active == True).all()
        
        for key_record in api_keys:
            # Compare hashes (constant-time comparison)
            if provided_hash == key_record.key_hash:
                # Update last used timestamp
                key_record.last_used_at = datetime.utcnow()
                db.commit()
                return key_record
        
        return None
    
    @staticmethod
    def list_api_keys(db: Session, user_id: int) -> List[APIKey]:
        """List user's API keys."""
        return db.query(APIKey).filter(
            APIKey.user_id == user_id
        ).order_by(APIKey.created_at.desc()).all()
    
    @staticmethod
    def revoke_api_key(db: Session, api_key_id: int, user_id: int) -> bool:
        """Revoke (deactivate) an API key."""
        api_key = db.query(APIKey).filter(
            APIKey.id == api_key_id,
            APIKey.user_id == user_id
        ).first()
        
        if not api_key:
            return False
        
        api_key.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def get_api_key(db: Session, api_key_id: int, user_id: int) -> Optional[APIKey]:
        """Get an API key by ID."""
        return db.query(APIKey).filter(
            APIKey.id == api_key_id,
            APIKey.user_id == user_id
        ).first()

