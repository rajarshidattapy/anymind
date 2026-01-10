"""Storage service for file operations."""
from pathlib import Path
from typing import Optional
from app.core.config import settings
from app.utils.hashing import calculate_file_hash


class StorageService:
    """Service for storage operations."""
    
    def __init__(self):
        self.storage_path = Path(settings.STORAGE_PATH)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def save_file(self, file_content: bytes, filename: str, subdirectory: str = "") -> Optional[Path]:
        """Save a file to storage."""
        target_dir = self.storage_path / subdirectory
        target_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = target_dir / filename
        try:
            file_path.write_bytes(file_content)
            return file_path
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    
    def get_file(self, filepath: str) -> Optional[bytes]:
        """Get file content."""
        file_path = self.storage_path / filepath
        if file_path.exists():
            return file_path.read_bytes()
        return None
    
    def delete_file(self, filepath: str) -> bool:
        """Delete a file."""
        file_path = self.storage_path / filepath
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    
    def get_file_hash(self, filepath: str) -> Optional[str]:
        """Get file hash."""
        file_path = self.storage_path / filepath
        if file_path.exists():
            return calculate_file_hash(file_path)
        return None

