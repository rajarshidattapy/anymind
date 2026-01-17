# Anymind SDK Documentation

Complete documentation for the Anymind Python SDK and CLI tool.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [CLI Commands](#cli-commands)
- [Python SDK](#python-sdk)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Advanced Usage](#advanced-usage)

## Overview

The Anymind SDK provides both a command-line interface (CLI) and a Python library for deploying and managing AI agents on the Anymind platform.

**Features:**
- Agent deployment via CLI
- Python SDK for programmatic access
- Configuration detection and validation
- Artifact packaging and upload
- Build status monitoring
- Log retrieval

## Installation

### From PyPI (when published)

```bash
pip install anymind
```

### From Source

```bash
cd anymind-sdk
pip install -e .
```

### Development Installation

```bash
cd anymind-sdk
pip install -e ".[dev]"
```

## Configuration

### anymind.yaml

The SDK looks for `anymind.yaml` in the current directory. This file defines your agent configuration.

**Required Fields:**
- `name`: Agent name (must be unique per user)
- `entrypoint`: Python entrypoint in format `module:function` (e.g., `agent.main:handle`)
- `framework`: Framework identifier (e.g., `python`)

**Optional Fields:**
- `description`: Agent description

**Example:**
```yaml
name: my-ai-agent
entrypoint: agent.main:handle
framework: python
description: A simple AI agent that processes text
```

### Environment Variables

**API Key:**
```bash
export ANYMIND_API_KEY=anymind_abc123...
```

**Base URL (optional):**
```bash
export ANYMIND_API_URL=http://localhost:8000
```

Default base URL: `http://localhost:8000`

### Project Structure

Your agent project should have this structure:

```
my-agent/
├── anymind.yaml          # Required: Agent configuration
├── requirements.txt       # Optional: Python dependencies
├── agent/
│   ├── __init__.py
│   └── main.py           # Contains handle() function
└── ...other files...
```

**Entrypoint Example:**
```python
# agent/main.py
def handle(payload: dict) -> dict:
    """
    Process agent input and return output.
    
    Args:
        payload: Input data from execution request
        
    Returns:
        dict: Output data
    """
    input_text = payload.get("input", "")
    result = process_input(input_text)
    return {"result": result}
```

## CLI Commands

### `anymind deploy`

Deploy an agent to Anymind. This command:
1. Validates `anymind.yaml`
2. Packages the project into `.tar.gz`
3. Creates or finds the agent
4. Uploads the artifact
5. Monitors build status

**Usage:**
```bash
anymind deploy
```

**Options:**
- `--api-key <key>`: API key (overrides `ANYMIND_API_KEY`)
- `--base-url <url>`: Base API URL (overrides `ANYMIND_API_URL`)

**Example:**
```bash
anymind deploy --api-key anymind_abc123...
```

**Output:**
```
Packaging agent...
Uploading artifact...
Uploaded
Building
Ready
Deployed agent: my-ai-agent (ID: 1)
Status: Ready
```

### `anymind status`

Get the status of an agent.

**Usage:**
```bash
anymind status
anymind status --agent-id 1
```

**Options:**
- `--agent-id <id>`: Agent ID (optional if in agent project directory)
- `--api-key <key>`: API key
- `--base-url <url>`: Base API URL

**Example:**
```bash
anymind status
```

**Output:**
```
Agent: my-ai-agent (ID: 1)
Status: Ready
Current Version: 5
```

### `anymind agents`

List all your agents.

**Usage:**
```bash
anymind agents
```

**Options:**
- `--api-key <key>`: API key
- `--base-url <url>`: Base API URL

**Example:**
```bash
anymind agents
```

**Output:**
```
   1  my-ai-agent                    Ready
   2  another-agent                  Building
   3  test-agent                     Draft
```

### `anymind logs`

Get logs for an agent (build logs and execution logs).

**Usage:**
```bash
anymind logs
anymind logs --agent-id 1
```

**Options:**
- `--agent-id <id>`: Agent ID (optional if in agent project directory)
- `--api-key <key>`: API key
- `--base-url <url>`: Base API URL

**Example:**
```bash
anymind logs --agent-id 1
```

**Output:**
```
2024-01-01 00:00:00 [INFO ] [build] Build v1: Build completed successfully
2024-01-01 12:00:00 [INFO ] [runtime] Execution 1 completed successfully
2024-01-01 12:05:00 [ERROR] [runtime] Execution 2 failed: Timeout error
```

## Python SDK

### AnymindClient

The main client class for interacting with the Anymind API.

**Initialization:**
```python
from anymind import AnymindClient
from anymind.auth import get_api_key, get_base_url

api_key = get_api_key()  # From env var or raise error
base_url = get_base_url()  # From env var or default
client = AnymindClient(api_key, base_url)
```

**Or with explicit values:**
```python
client = AnymindClient(
    api_key="anymind_abc123...",
    base_url="http://localhost:8000"
)
```

### Agent Management

#### Create Agent

```python
agent = client.create_agent(
    name="my-agent",
    description="My AI agent"
)
print(f"Created agent: {agent['id']}")
```

#### List Agents

```python
agents = client.list_agents()
for agent in agents:
    print(f"{agent['id']}: {agent['name']} - {agent['status']}")
```

#### Get Agent

```python
agent = client.get_agent(agent_id=1)
print(f"Agent: {agent['name']}, Status: {agent['status']}")
```

#### Find Agent by Name

```python
agent = client.find_agent_by_name("my-agent")
if agent:
    print(f"Found agent: {agent['id']}")
else:
    print("Agent not found")
```

### Artifact Upload

```python
version = client.upload_artifact(
    agent_id=1,
    tarball_path="/path/to/agent.tar.gz"
)
print(f"Uploaded version: {version['id']}, Status: {version['status']}")
```

### Logs

```python
logs = client.get_agent_logs(agent_id=1)
for log in logs:
    print(f"{log['timestamp']} [{log['level']}] {log['message']}")
```

### Agent Status

```python
status = client.get_agent_status(agent_id=1)
print(f"Status: {status['status']}")
print(f"Current Version: {status.get('current_version_id')}")
```

## Examples

### Complete Deployment Script

```python
from anymind import AnymindClient
from anymind.auth import get_api_key, get_base_url
from anymind.config import load_config, get_project_root
from anymind.packaging import package_agent
from anymind.deploy import deploy

# Load configuration
config = load_config()
project_root = get_project_root()

# Initialize client
client = AnymindClient(get_api_key(), get_base_url())

# Deploy
result = deploy(
    client,
    project_root=project_root,
    on_progress=lambda msg: print(f"Progress: {msg}"),
    on_status=lambda status: print(f"Status: {status}")
)

print(f"Deployed: {result['agent_name']} (ID: {result['agent_id']})")
```

### Custom Deployment with Status Polling

```python
import time
from anymind import AnymindClient
from anymind.auth import get_api_key, get_base_url
from anymind.config import load_config
from anymind.packaging import package_agent
from anymind.deploy import ensure_agent_exists, upload_with_progress

client = AnymindClient(get_api_key(), get_base_url())
config = load_config()

# Ensure agent exists
agent = ensure_agent_exists(client, config["name"], config.get("description"))
print(f"Agent ID: {agent['id']}")

# Package
tarball_path = package_agent(get_project_root())
print(f"Packaged: {tarball_path}")

# Upload
version = upload_with_progress(
    client,
    agent["id"],
    tarball_path,
    on_progress=lambda msg: print(msg)
)
print(f"Version ID: {version['id']}, Status: {version['status']}")

# Poll for build completion
while True:
    agent = client.get_agent(agent["id"])
    status = agent["status"]
    print(f"Current status: {status}")
    
    if status in ["ready", "failed"]:
        break
    
    time.sleep(2)
```

### Batch Agent Operations

```python
from anymind import AnymindClient
from anymind.auth import get_api_key, get_base_url

client = AnymindClient(get_api_key(), get_base_url())

# List all agents and their statuses
agents = client.list_agents()
for agent in agents:
    print(f"{agent['name']}: {agent['status']}")
    
    # Get logs for each agent
    logs = client.get_agent_logs(agent['id'])
    print(f"  Logs: {len(logs)} entries")
```

### Error Handling Example

```python
from anymind import AnymindClient
from anymind.exceptions import (
    ConfigurationError,
    AuthenticationError,
    APIError,
    DeploymentError
)

try:
    client = AnymindClient(get_api_key(), get_base_url())
    agents = client.list_agents()
except AuthenticationError as e:
    print(f"Auth failed: {e}")
except APIError as e:
    print(f"API error ({e.status_code}): {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Error Handling

### Exception Hierarchy

```
AnymindError (base)
├── ConfigurationError
├── AuthenticationError
├── APIError
└── DeploymentError
```

### ConfigurationError

Raised when `anymind.yaml` is missing or invalid.

```python
from anymind.exceptions import ConfigurationError
from anymind.config import load_config

try:
    config = load_config()
except ConfigurationError as e:
    print(f"Config error: {e}")
```

### AuthenticationError

Raised when API key is missing or invalid.

```python
from anymind.exceptions import AuthenticationError
from anymind.auth import get_api_key

try:
    api_key = get_api_key()
except AuthenticationError as e:
    print(f"Auth error: {e}")
```

### APIError

Raised when API request fails.

```python
from anymind.exceptions import APIError

try:
    agent = client.get_agent(999)
except APIError as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
    print(f"Response: {e.response}")
```

### DeploymentError

Raised when deployment fails.

```python
from anymind.exceptions import DeploymentError
from anymind.deploy import deploy

try:
    result = deploy(client)
except DeploymentError as e:
    print(f"Deployment failed: {e}")
```

## Advanced Usage

### Custom Packaging

```python
from anymind.packaging import create_tarball, get_exclude_patterns
from pathlib import Path

# Custom exclude patterns
exclude = get_exclude_patterns()
exclude.add("custom_exclude_pattern")

# Create tarball
tarball_path = create_tarball(
    source_dir=Path("."),
    output_path=Path("custom-agent.tar.gz"),
    exclude_patterns=exclude
)
```

### Direct API Calls

For advanced use cases, you can make direct API calls:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/agents",
    headers={"X-API-Key": "your-key"},
    json={"name": "my-agent"}
)
agent = response.json()
```

### Configuration Validation

```python
from anymind.config import load_config, find_anymind_yaml

# Find config file
yaml_path = find_anymind_yaml()

# Load and validate
config = load_config(yaml_path)

# Access configuration
print(f"Agent name: {config['name']}")
print(f"Entrypoint: {config['entrypoint']}")
```

### Utility Functions

```python
from anymind.utils import format_timestamp, format_log_entry, format_status

# Format timestamp
timestamp = format_timestamp("2024-01-01T00:00:00")
# Output: "2024-01-01 00:00:00"

# Format log entry
log = {
    "timestamp": "2024-01-01T00:00:00",
    "level": "INFO",
    "message": "Build completed",
    "source": "build"
}
formatted = format_log_entry(log)
# Output: "2024-01-01 00:00:00 [INFO ] [build] Build completed"

# Format status
status = format_status("ready")
# Output: "Ready"
```

## Package Structure

The SDK is organized as follows:

```
anymind/
├── __init__.py          # Package exports
├── cli.py               # CLI interface (Typer)
├── client.py            # HTTP client
├── config.py           # Configuration detection
├── deploy.py            # Deployment logic
├── packaging.py         # Tarball creation
├── auth.py              # Authentication
├── exceptions.py         # Custom exceptions
└── utils.py              # Utility functions
```

## Best Practices

### 1. Always Validate Configuration

```python
from anymind.config import load_config

try:
    config = load_config()
except ConfigurationError as e:
    print(f"Invalid configuration: {e}")
    exit(1)
```

### 2. Handle Errors Gracefully

```python
from anymind.exceptions import AnymindError

try:
    result = deploy(client)
except AnymindError as e:
    print(f"Error: {e}")
    exit(1)
```

### 3. Use Environment Variables

```bash
# .env or shell
export ANYMIND_API_KEY=your-key
export ANYMIND_API_URL=http://localhost:8000
```

### 4. Package Only What's Needed

Ensure your `.gitignore` excludes unnecessary files, and the SDK will automatically exclude common patterns like `.git`, `__pycache__`, `.venv`, etc.

### 5. Monitor Build Status

```python
import time

version = client.upload_artifact(agent_id, tarball_path)
while True:
    agent = client.get_agent(agent_id)
    if agent["status"] in ["ready", "failed"]:
        break
    time.sleep(2)
```

## Troubleshooting

### "anymind.yaml not found"

**Solution:** Make sure you're in the agent project directory, or specify the path.

### "API key required"

**Solution:** Set `ANYMIND_API_KEY` environment variable or use `--api-key` flag.

### "Invalid API key"

**Solution:** Verify your API key is correct. Create a new one via the web UI if needed.

### "Build failed"

**Solution:** Check the build logs:
```bash
anymind logs --agent-id <id>
```

Common issues:
- Missing `anymind.yaml` in artifact
- Invalid entrypoint format
- Entrypoint function not found
- Import errors in agent code

### "Execution timeout"

**Solution:** Your agent execution exceeded 30 seconds. Optimize your code or break it into smaller operations.

## Development

### Running Tests

```bash
cd anymind-sdk
pytest
```

### Code Formatting

```bash
black anymind/
```

### Linting

```bash
ruff anymind/
```

### Building Distribution

```bash
python setup.py sdist bdist_wheel
```

## License

MIT

