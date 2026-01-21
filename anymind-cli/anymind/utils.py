"""Utility functions."""
from typing import Any, Dict
from datetime import datetime


def format_timestamp(timestamp: Any) -> str:
    """Format timestamp for display."""
    if isinstance(timestamp, str):
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return timestamp
    elif isinstance(timestamp, datetime):
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return str(timestamp)


def format_log_entry(entry: Dict[str, Any]) -> str:
    """Format log entry for display."""
    timestamp = format_timestamp(entry.get("timestamp", ""))
    level = entry.get("level", "INFO").ljust(5)
    message = entry.get("message", "")
    source = entry.get("source", "")
    
    if source:
        return f"{timestamp} [{level}] [{source}] {message}"
    return f"{timestamp} [{level}] {message}"


def format_status(status: str) -> str:
    """Format status for display."""
    status_map = {
        "draft": "Draft",
        "building": "Building",
        "ready": "Ready",
        "failed": "Failed",
        "archived": "Archived",
        "queued": "Queued",
    }
    return status_map.get(status.lower(), status.capitalize())

