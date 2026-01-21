"""Setup script for anymind package."""
from setuptools import setup, find_packages

setup(
    name="anymind",
    version="0.1.0",
    description="Anymind Python SDK and CLI for deploying AI agents",
    long_description=open("README.md").read() if __import__("pathlib").Path("README.md").exists() else "",
    long_description_content_type="text/markdown",
    author="Anymind",
    author_email="support@anymind.com",
    url="https://github.com/anymind/anymind-sdk",
    packages=find_packages(),
    install_requires=[
        "typer>=0.9.0",
        "requests>=2.31.0",
        "pyyaml>=6.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "anymind=anymind.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

