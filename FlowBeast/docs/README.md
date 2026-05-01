# FlowBeast Documentation

This directory contains MkDocs-generated documentation for FlowBeast.

## Quick Start

```bash
# Install dependencies
uv add mkdocs mkdocs-material

# Serve documentation locally
mkdocs serve

# Build production site
mkdocs build
```

## Directory Structure

```
docs/
├── index.md           # Homepage
├── getting-started.md # Installation guide
├── architecture.md    # System architecture
├── tech-debt.md       # Tech debt and roadmap
├── adrs/              # Architecture Decision Records
│   ├── index.md
│   └── *.md
├── ideas/             # Working notes (for developers)
├── meetings/          # Meeting notes (for developers)
└── technical_reports/ # Experiment reports (for developers)
```

## For Developers

- **Project docs** (`docs/`): User-facing documentation, served at `https://flowbeast.ai`
- **FlowBeast docs** (`flowbeast/docs/`): Internal technical documentation

## Related

- [CLAUDE.md](../CLAUDE.md) - AI assistant instructions
- [README.md](../README.md) - Project overview
- [flowbeast/docs/](../flowbeast/docs/) - Internal docs
