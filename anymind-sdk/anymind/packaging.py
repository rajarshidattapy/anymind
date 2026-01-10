"""Agent packaging utilities."""
import tarfile
import tempfile
from pathlib import Path
from typing import List, Set


def get_exclude_patterns() -> Set[str]:
    """Get patterns to exclude from package."""
    return {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "env",
        ".env",
        ".env.local",
        ".env.*.local",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "node_modules",
        ".DS_Store",
        "*.log",
        ".idea",
        ".vscode",
    }


def should_exclude(path: Path, exclude_patterns: Set[str]) -> bool:
    """Check if path should be excluded."""
    path_str = str(path)
    
    # Check if any part of the path matches exclude patterns
    for part in path.parts:
        if part in exclude_patterns:
            return True
    
    # Check if path ends with excluded extension
    if path.suffix in {".pyc", ".pyo", ".pyd"}:
        return True
    
    # Check if path matches any pattern
    for pattern in exclude_patterns:
        if pattern in path_str:
            return True
    
    return False


def create_tarball(
    source_dir: Path,
    output_path: Path,
    exclude_patterns: Set[str] = None
) -> Path:
    """Create a tarball from source directory."""
    if exclude_patterns is None:
        exclude_patterns = get_exclude_patterns()
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Required files that should always be included
    required_files = {"anymind.yaml", "requirements.txt"}
    
    with tarfile.open(output_path, "w:gz") as tar:
        # Add all files, excluding patterns
        for item in source_dir.rglob("*"):
            # Always include required files
            if item.name in required_files:
                arcname = item.relative_to(source_dir)
                tar.add(item, arcname=arcname)
                continue
            
            if should_exclude(item, exclude_patterns):
                continue
            
            if item.is_file():
                # Get relative path for archive
                arcname = item.relative_to(source_dir)
                tar.add(item, arcname=arcname)
    
    return output_path


def package_agent(project_root: Path, output_dir: Path = None) -> Path:
    """Package agent project into tarball."""
    if output_dir is None:
        output_dir = tempfile.mkdtemp()
    
    output_dir = Path(output_dir)
    output_path = output_dir / "agent.tar.gz"
    
    create_tarball(project_root, output_path)
    
    return output_path

