"""Rate limiting and quota utilities."""
from typing import Optional
from datetime import datetime, timedelta
from collections import defaultdict


class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self):
        self.requests: dict[str, list[datetime]] = defaultdict(list)
    
    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> bool:
        """Check if a request is allowed."""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_seconds)
        
        # Clean old requests
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > window_start
        ]
        
        # Check limit
        if len(self.requests[key]) >= max_requests:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()


def check_rate_limit(user_id: int, max_requests: int = 100, window_seconds: int = 60) -> bool:
    """Check if user has exceeded rate limit."""
    return rate_limiter.is_allowed(f"user_{user_id}", max_requests, window_seconds)

