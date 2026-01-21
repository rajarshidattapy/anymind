"""CLI interface using Typer."""
import typer
from typing import Optional
from pathlib import Path
from anymind.auth import get_api_key, get_base_url
from anymind.client import AnymindClient
from anymind.deploy import deploy
from anymind.config import load_config, get_project_root
from anymind.exceptions import (
    AnymindError,
    ConfigurationError,
    AuthenticationError,
    APIError,
    DeploymentError,
)
from anymind.utils import format_log_entry, format_status

app = typer.Typer(help="Anymind CLI - Deploy and manage AI agents")


def handle_error(e: Exception):
    """Handle and display errors."""
    if isinstance(e, ConfigurationError):
        typer.echo(f"Configuration error: {e}", err=True)
    elif isinstance(e, AuthenticationError):
        typer.echo(f"Authentication error: {e}", err=True)
    elif isinstance(e, APIError):
        typer.echo(f"API error: {e}", err=True)
        if e.status_code:
            typer.echo(f"Status code: {e.status_code}", err=True)
    elif isinstance(e, DeploymentError):
        typer.echo(f"Deployment error: {e}", err=True)
    elif isinstance(e, AnymindError):
        typer.echo(f"Error: {e}", err=True)
    else:
        typer.echo(f"Unexpected error: {e}", err=True)
    
    raise typer.Exit(1)


@app.command()
def deploy_cmd(
    api_key: Optional[str] = typer.Option(None, "--api-key", "-k", help="API key"),
    base_url: Optional[str] = typer.Option(None, "--base-url", "-u", help="Base API URL"),
):
    """Deploy agent to Anymind."""
    try:
        api_key = get_api_key(api_key)
        base_url = get_base_url(base_url)
        
        client = AnymindClient(api_key, base_url)
        
        def on_progress(message: str):
            typer.echo(message)
        
        def on_status(message: str):
            typer.echo(message)
        
        result = deploy(client, on_progress=on_progress, on_status=on_status)
        
        typer.echo(f"Deployed agent: {result['agent_name']} (ID: {result['agent_id']})")
        typer.echo(f"Status: {format_status(result['status'])}")
        
    except Exception as e:
        handle_error(e)


@app.command()
def status(
    agent_id: Optional[int] = typer.Option(None, "--agent-id", "-a", help="Agent ID"),
    api_key: Optional[str] = typer.Option(None, "--api-key", "-k", help="API key"),
    base_url: Optional[str] = typer.Option(None, "--base-url", "-u", help="Base API URL"),
):
    """Get agent status."""
    try:
        api_key = get_api_key(api_key)
        base_url = get_base_url(base_url)
        
        client = AnymindClient(api_key, base_url)
        
        if agent_id is None:
            # Try to get agent ID from config
            try:
                config = load_config()
                agent_name = config["name"]
                agent = client.find_agent_by_name(agent_name)
                if agent:
                    agent_id = agent["id"]
                else:
                    typer.echo(f"Agent '{agent_name}' not found", err=True)
                    raise typer.Exit(1)
            except ConfigurationError:
                typer.echo("Agent ID required when not in agent project directory", err=True)
                raise typer.Exit(1)
        
        status_info = client.get_agent_status(agent_id)
        
        typer.echo(f"Agent: {status_info['name']} (ID: {status_info['id']})")
        typer.echo(f"Status: {format_status(status_info['status'])}")
        if status_info.get("current_version_id"):
            typer.echo(f"Current Version: {status_info['current_version_id']}")
        
    except Exception as e:
        handle_error(e)


@app.command()
def agents(
    api_key: Optional[str] = typer.Option(None, "--api-key", "-k", help="API key"),
    base_url: Optional[str] = typer.Option(None, "--base-url", "-u", help="Base API URL"),
):
    """List all agents."""
    try:
        api_key = get_api_key(api_key)
        base_url = get_base_url(base_url)
        
        client = AnymindClient(api_key, base_url)
        agents = client.list_agents()
        
        if not agents:
            typer.echo("No agents found")
            return
        
        for agent in agents:
            status_str = format_status(agent.get("status", "unknown"))
            typer.echo(f"{agent['id']:4d}  {agent['name']:30s}  {status_str}")
        
    except Exception as e:
        handle_error(e)


@app.command()
def logs(
    agent_id: Optional[int] = typer.Option(None, "--agent-id", "-a", help="Agent ID"),
    api_key: Optional[str] = typer.Option(None, "--api-key", "-k", help="API key"),
    base_url: Optional[str] = typer.Option(None, "--base-url", "-u", help="Base API URL"),
):
    """Get agent logs."""
    try:
        api_key = get_api_key(api_key)
        base_url = get_base_url(base_url)
        
        client = AnymindClient(api_key, base_url)
        
        if agent_id is None:
            # Try to get agent ID from config
            try:
                config = load_config()
                agent_name = config["name"]
                agent = client.find_agent_by_name(agent_name)
                if agent:
                    agent_id = agent["id"]
                else:
                    typer.echo(f"Agent '{agent_name}' not found", err=True)
                    raise typer.Exit(1)
            except ConfigurationError:
                typer.echo("Agent ID required when not in agent project directory", err=True)
                raise typer.Exit(1)
        
        logs = client.get_agent_logs(agent_id)
        
        if not logs:
            typer.echo("No logs found")
            return
        
        for entry in logs:
            typer.echo(format_log_entry(entry))
        
    except Exception as e:
        handle_error(e)


def main():
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    main()

