# Anymind Python SDK

Python SDK and CLI for deploying AI agents to the Anymind platform.

## Installation

```bash
pip install anymind
```

Or install from source:

```bash
cd anymind-sdk
pip install -e .
```

## Quick Start

1. Create an `anymind.yaml` file in your agent project:

```yaml
name: my-agent
entrypoint: agent.main:handle
framework: python
description: My awesome AI agent
```

2. Set your API key:

```bash
export ANYMIND_API_KEY=your-api-key-here
```

3. Deploy your agent:

```bash
anymind deploy
```

## Configuration

The SDK looks for `anymind.yaml` in the current directory. Required fields:

- `name`: Agent name
- `entrypoint`: Python entrypoint in format `module:function` (e.g., `agent.main:handle`)
- `framework`: Framework identifier (e.g., `python`)

Optional fields:

- `description`: Agent description

## CLI Commands

### `anymind deploy`

Deploy an agent to Anymind. Packages the current directory and uploads it.

Options:
- `--api-key`: API key (or set `ANYMIND_API_KEY` env var)
- `--base-url`: Base API URL (default: `http://localhost:8000`, or set `ANYMIND_API_URL` env var)

### `anymind status`

Get the status of an agent.

Options:
- `--agent-id`: Agent ID (optional if in agent project directory)
- `--api-key`: API key
- `--base-url`: Base API URL

### `anymind agents`

List all your agents.

Options:
- `--api-key`: API key
- `--base-url`: Base API URL

### `anymind logs`

Get logs for an agent.

Options:
- `--agent-id`: Agent ID (optional if in agent project directory)
- `--api-key`: API key
- `--base-url`: Base API URL

## Python SDK

You can also use the SDK programmatically:

```python
from anymind import AnymindClient
from anymind.auth import get_api_key, get_base_url

api_key = get_api_key()
base_url = get_base_url()
client = AnymindClient(api_key, base_url)

# List agents
agents = client.list_agents()

# Get agent
agent = client.get_agent(agent_id=1)

# Get logs
logs = client.get_agent_logs(agent_id=1)
```

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black anymind/

# Lint code
ruff anymind/
```

## License

MIT

