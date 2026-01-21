"""Tarball utilities."""
import tarfile
import tempfile
from pathlib import Path
from typing import Optional
import shutil


def create_tarball(source_dir: Path, output_path: Path) -> bool:
    """Create a tarball from a source directory."""
    try:
        with tarfile.open(output_path, "w:gz") as tar:
            tar.add(source_dir, arcname=source_dir.name)
        return True
    except Exception as e:
        print(f"Error creating tarball: {e}")
        return False


def extract_tarball(tarball_path: Path, output_dir: Path) -> bool:
    """Extract a tarball to a directory."""
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        with tarfile.open(tarball_path, "r:gz") as tar:
            tar.extractall(output_dir)
        return True
    except Exception as e:
        print(f"Error extracting tarball: {e}")
        return False


def validate_tarball(tarball_path: Path) -> bool:
    """Validate that a tarball can be opened."""
    try:
        with tarfile.open(tarball_path, "r:gz") as tar:
            tar.getmembers()
        return True
    except Exception:
        return False

