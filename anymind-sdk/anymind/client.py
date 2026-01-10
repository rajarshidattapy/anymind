"""HTTP client for Anymind API."""
import requests
from pathlib import Path
from typing import Dict, Any, Optional, List
from anymind.exceptions import APIError, AuthenticationError


class AnymindClient:
    """Client for interacting with Anymind API."""
    
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "Content-Type": "application/json",
        })
    
    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """Make HTTP request with error handling."""
        url = f"{self.base_url}/api/v1{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status_code == 404:
                raise APIError(f"Resource not found: {endpoint}", 404)
            elif not response.ok:
                error_msg = f"API request failed: {response.status_code}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg = error_data["detail"]
                except:
                    error_msg = response.text or error_msg
                
                raise APIError(error_msg, response.status_code, response.json() if response.content else None)
            
            return response
        except requests.exceptions.RequestException as e:
            raise APIError(f"Network error: {str(e)}")
    
    def create_agent(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Create a new agent."""
        data = {"name": name}
        if description:
            data["description"] = description
        
        response = self._request("POST", "/agents", json=data)
        return response.json()
    
    def list_agents(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """List user's agents."""
        params = {"skip": skip, "limit": limit}
        response = self._request("GET", "/agents", params=params)
        return response.json()
    
    def get_agent(self, agent_id: int) -> Dict[str, Any]:
        """Get agent by ID."""
        response = self._request("GET", f"/agents/{agent_id}")
        return response.json()
    
    def find_agent_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find agent by name."""
        agents = self.list_agents()
        for agent in agents:
            if agent.get("name") == name:
                return agent
        return None
    
    def upload_artifact(self, agent_id: int, tarball_path: str) -> Dict[str, Any]:
        """Upload agent artifact."""
        # Remove Content-Type header for file upload
        headers = self.session.headers.copy()
        headers.pop("Content-Type", None)
        
        with open(tarball_path, 'rb') as f:
            files = {"file": (Path(tarball_path).name, f, "application/gzip")}
            response = self.session.post(
                f"{self.base_url}/api/v1/uploads/agent/{agent_id}",
                files=files,
                headers=headers
            )
            
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status_code == 404:
                raise APIError(f"Agent not found: {agent_id}", 404)
            elif not response.ok:
                error_msg = f"Upload failed: {response.status_code}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg = error_data["detail"]
                except:
                    error_msg = response.text or error_msg
                raise APIError(error_msg, response.status_code)
            
            return response.json()
    
    def get_agent_logs(self, agent_id: int) -> List[Dict[str, Any]]:
        """Get logs for an agent."""
        response = self._request("GET", f"/logs/{agent_id}")
        return response.json()
    
    def get_agent_status(self, agent_id: int) -> Dict[str, Any]:
        """Get agent status and latest version."""
        agent = self.get_agent(agent_id)
        return {
            "id": agent["id"],
            "name": agent["name"],
            "status": agent["status"],
            "current_version_id": agent.get("current_version_id"),
        }

