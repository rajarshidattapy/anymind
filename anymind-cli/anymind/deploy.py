"""Deployment logic."""
import time
from pathlib import Path
from typing import Dict, Any, Optional
from anymind.client import AnymindClient
from anymind.config import load_config, get_project_root
from anymind.packaging import package_agent
from anymind.exceptions import DeploymentError, ConfigurationError


def ensure_agent_exists(client: AnymindClient, agent_name: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Ensure agent exists, create if it doesn't."""
    # Try to find existing agent
    agent = client.find_agent_by_name(agent_name)
    
    if agent:
        return agent
    
    # Create new agent
    return client.create_agent(agent_name, description)


def upload_with_progress(client: AnymindClient, agent_id: int, tarball_path: Path, on_progress=None):
    """Upload artifact with progress callback."""
    if on_progress:
        on_progress("Uploading artifact...")
    
    result = client.upload_artifact(agent_id, str(tarball_path))
    
    if on_progress:
        on_progress("Uploaded")
    
    return result


def wait_for_build(client: AnymindClient, agent_id: int, version_id: int, on_status=None, timeout: int = 300) -> Dict[str, Any]:
    """Wait for build to complete."""
    start_time = time.time()
    last_status = None
    
    if on_status:
        on_status("Building")
    
    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise DeploymentError(f"Build timeout after {timeout} seconds")
        
        # Get agent to check status
        try:
            agent = client.get_agent(agent_id)
            current_status = agent.get("status", "unknown")
            
            # Update status message if changed
            if current_status != last_status:
                if on_status:
                    on_status(current_status.capitalize())
                last_status = current_status
            
            # Check if build is complete
            if current_status in ["ready", "failed"]:
                if current_status == "failed":
                    raise DeploymentError("Build failed. Check logs for details.")
                return {"status": "ready", "version_id": version_id}
            
        except Exception as e:
            # If we can't check status, continue polling
            pass
        
        time.sleep(2)


def deploy(
    client: AnymindClient,
    project_root: Path = None,
    on_progress=None,
    on_status=None
) -> Dict[str, Any]:
    """Deploy agent to Anymind."""
    # Load configuration
    try:
        config = load_config()
    except ConfigurationError as e:
        raise DeploymentError(f"Configuration error: {e}")
    
    if project_root is None:
        project_root = get_project_root()
    
    # Ensure agent exists
    agent_name = config["name"]
    agent_description = config.get("description")
    
    try:
        agent = ensure_agent_exists(client, agent_name, agent_description)
        agent_id = agent["id"]
    except Exception as e:
        raise DeploymentError(f"Failed to create/find agent: {e}")
    
    # Package agent
    try:
        if on_progress:
            on_progress("Packaging agent...")
        
        tarball_path = package_agent(project_root)
    except Exception as e:
        raise DeploymentError(f"Failed to package agent: {e}")
    
    # Upload artifact
    try:
        version = upload_with_progress(client, agent_id, tarball_path, on_progress)
        version_id = version.get("id")
    except Exception as e:
        raise DeploymentError(f"Failed to upload artifact: {e}")
    
    # Wait for build (simplified - in production would poll version status)
    try:
        build_result = wait_for_build(client, agent_id, version_id, on_status)
    except Exception as e:
        raise DeploymentError(f"Build failed: {e}")
    
    return {
        "agent_id": agent_id,
        "agent_name": agent_name,
        "version_id": version_id,
        "status": build_result["status"],
    }

