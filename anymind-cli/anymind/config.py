"""Configuration detection and validation."""
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from anymind.exceptions import ConfigurationError


def find_anymind_yaml(directory: Path = None) -> Path:
    """Find anymind.yaml in the current or specified directory."""
    if directory is None:
        directory = Path.cwd()
    
    yaml_path = directory / "anymind.yaml"
    if not yaml_path.exists():
        raise ConfigurationError(
            f"anymind.yaml not found in {directory}. "
            "Make sure you're in the agent project directory."
        )
    
    return yaml_path


def load_config(yaml_path: Path = None) -> Dict[str, Any]:
    """Load and validate anymind.yaml configuration."""
    if yaml_path is None:
        yaml_path = find_anymind_yaml()
    
    try:
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigurationError(f"Failed to parse anymind.yaml: {e}")
    except Exception as e:
        raise ConfigurationError(f"Failed to read anymind.yaml: {e}")
    
    if not isinstance(config, dict):
        raise ConfigurationError("anymind.yaml must be a YAML object")
    
    # Validate required fields
    required_fields = ["name", "entrypoint", "framework"]
    missing_fields = [field for field in required_fields if field not in config]
    
    if missing_fields:
        raise ConfigurationError(
            f"Missing required fields in anymind.yaml: {', '.join(missing_fields)}"
        )
    
    # Validate entrypoint format
    entrypoint = config.get("entrypoint", "")
    if ":" not in entrypoint:
        raise ConfigurationError(
            "entrypoint must be in format 'module:function' (e.g., 'agent.main:handle')"
        )
    
    return config


def get_project_root(yaml_path: Path = None) -> Path:
    """Get the project root directory (where anymind.yaml is located)."""
    if yaml_path is None:
        yaml_path = find_anymind_yaml()
    return yaml_path.parent

