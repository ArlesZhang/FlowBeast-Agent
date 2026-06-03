# FlowBeast DevContainer

This directory contains the VS Code DevContainer configuration for FlowBeast development.

## Structure

- `devcontainer.json` - VS Code DevContainer configuration
- `docker-compose.extend.yml` - Docker Compose override for development

## Features

- **Python 3.12** with `uv` for fast dependency management
- **Non-root user** (`vscode`) for security
- **Hot reload** support for development
- **Pre-configured VS Code extensions**:
  - Python extension with Pylance
  - Ruff for linting and formatting
  - Even Better TOML
  - Docker extension

## Usage

1. Open the project in VS Code
2. Press `F1` and select `Dev Containers: Reopen in Container`
3. Wait for the container to build (first time may take a few minutes)
4. The development environment is ready!

## Post-Create Commands

The following commands run automatically after the container is created:

- `uv sync` - Install dependencies from `uv.lock`

## Development Workflow

Inside the container:

```bash
# Run the drama generation pipeline
python main.py

# Run the FastAPI server
uvicorn flowbeast.api.main:app --reload --port 8000

# Run tests
uv run pytest tests/ -q

# Seed FP3 (ViralUnit + PromptAtom)
uv run python -m flowbeast.fp3.seed_data
```

## Troubleshooting

### Permission Issues

If you encounter permission issues with file ownership, the container uses `updateRemoteUserUID: true` in `devcontainer.json` to match your local user ID.

### Rebuilding the Container

If you need to rebuild the container (e.g., after changes to Dockerfile):

1. Press `F1` and select `Dev Containers: Rebuild Container`

### Resetting the Container

To start fresh:

1. Press `F1` and select `Dev Containers: Reopen Folder Locally`
2. Then `Dev Containers: Rebuild and Reopen in Container`

## Configuration Details

The devcontainer uses:
- **Base Image**: `python:3.12-slim`
- **User**: `vscode` (non-root)
- **Working Directory**: `/app`
- **Package Manager**: `uv`
- **Port**: `8000` (forwarded to host)
