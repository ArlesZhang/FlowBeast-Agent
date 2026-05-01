# FlowBeast

**AI-powered short-form drama content generation engine**

> **FlowBeast** is an AI-powered short-form drama content generation engine. The core pipeline is: **Topic → Viral Script (JSON) → Audio → Video-ready output**.

---

## Quick Links

- 📚 [Getting Started](getting-started.md)
- 🏗️ [Architecture](architecture.md)
- 🚀 [Quick Start](getting-started.md)

## Features

- 🎬 **Drama Generation**: AI-driven short drama script generation
- 🧬 **FP3 Knowledge Base**: RAG-powered viral pattern injection
- 🎙️ **Audio Generation**: TTS-powered voice synthesis
- 🎥 **Video Pipeline**: End-to-end video generation

## Project Structure

```
FlowBeast/
├── flowbeast/          # Core package
│   ├── drama/         # Drama generation engine
│   ├── fp3/           # RAG knowledge base
│   ├── core/          # Core utilities
│   └── api/           # FastAPI server
├── docs/              # MkDocs documentation
├── scripts/           # Utility scripts
└── tests/             # Test suite
```

## Commands

```bash
# Install dependencies
uv sync

# Run the drama generation pipeline
python main.py

# Run the FastAPI server
uvicorn flowbeast.api.main:app --reload --port 8000

# Initialize FP3 vector knowledge base
python -m scripts.init_fp3

# Run tests
uv run pytest tests/ -q
```

## Resources

- 📖 [Documentation](getting-started.md)
- 💬 [Discussions](https://github.com/FlowBeast/FlowBeast/discussions)
- 🐛 [Issues](https://github.com/FlowBeast/FlowBeast/issues)

---

**Version**: 0.3.2 (FP3 Quality Control)
