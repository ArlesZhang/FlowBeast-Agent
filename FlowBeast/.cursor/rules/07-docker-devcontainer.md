# FlowBeast Docker & DevContainer Rules

> Container environment guidelines

## Environment Philosophy

- Reproducible development
- Local-first workflows
- Stable container environments

## Docker

Dockerfiles should:
- Be minimal
- Be cache-friendly
- Avoid unnecessary layers
- Preserve readability

Avoid:
- Huge all-in-one images
- Unnecessary system packages

## Dev Containers

Devcontainer environments must:
- Mirror production reasonably
- Support VS Code workflows
- Support AI coding tools
- Preserve bind mount behavior

## Volumes and Mounts

Understand:
- `/app` is bind-mounted from host
- File changes are real-time
- Containers are ephemeral
- Source code lives on host filesystem

## Networking

Support:
- Proxy configuration
- OpenAI-compatible APIs
- OpenRouter
- Local model providers (e.g., Ollama)

## Scripts

Scripts should:
- Be idempotent
- Be readable
- Fail loudly
- Avoid destructive defaults
