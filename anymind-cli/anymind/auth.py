"""Authentication handling."""
import os
from typing import Optional
from anymind.exceptions import AuthenticationError


def get_api_key(api_key: Optional[str] = None) -> str:
    """Get API key from flag or environment variable."""
    if api_key:
        return api_key
    
    env_key = os.getenv("ANYMIND_API_KEY")
    if not env_key:
        raise AuthenticationError(
            "API key required. Set --api-key flag or ANYMIND_API_KEY environment variable."
        )
    
    return env_key


def get_base_url(base_url: Optional[str] = None) -> str:
    """Get base URL from flag or environment variable."""
    if base_url:
        return base_url.rstrip('/')
    
    env_url = os.getenv("ANYMIND_API_URL", "http://localhost:8000")
    return env_url.rstrip('/')

