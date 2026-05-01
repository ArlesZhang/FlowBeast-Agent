# Getting Started

Welcome to FlowBeast! This guide will help you get up and running quickly.

## Prerequisites

- Python 3.10+
- `uv` package manager
- API keys for your chosen LLM provider

## Installation

```bash
# Clone the repository
git clone https://github.com/FlowBeast/FlowBeast.git
cd FlowBeast

# Install dependencies
uv sync
```

## Configuration

Create a `.env` file in the project root:

```bash
# LLM Provider (gemini, qwen, openai, openrouter, ollama)
ACTIVE_VENDOR=gemini

# API Keys
GOOGLE_API_KEY=your_google_api_key
# DASHSCOPE_API_KEY=your_dashscope_key
# OPENAI_API_KEY=your_openai_key

# Output directories
FLOWBEAST_OUTPUT_DIR=./flowbeast/data/outputs
FLOWBEAST_VECTOR_DIR=./flowbeast/data/vectors
```

## First Run

```bash
# Initialize FP3 knowledge base (first-time setup)
python -m scripts.init_fp3

# Run the drama generation pipeline
python main.py --topic "一个关于人工智能的短剧"
```

## Available Commands

| Command | Description |
|---------|-------------|
| `python main.py` | Run full pipeline |
| `uvicorn flowbeast.api.main:app --reload` | Start API server |
| `uv run pytest tests/` | Run tests |
| `mkdocs serve` | Preview docs locally |

## next steps

- 📖 Read the [Architecture](architecture.md) docs
- 🔧 Check out [Tech Debt](tech-debt.md) for known issues
- 📚 Explore \[ADRs\](adrs/index.md) for architectural decisions
