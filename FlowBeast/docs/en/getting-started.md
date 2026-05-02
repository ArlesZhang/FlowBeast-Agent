# Getting Started

Welcome to FlowBeast! This guide will help you get up and running quickly.

## Prerequisites

- Python 3.10+
- `uv` package manager
- API keys for your chosen LLM provider

## Installation

```bash
git clone https://github.com/FlowBeast/FlowBeast.git
cd FlowBeast
uv sync
```

## Configuration

Create a `.env` file in the project root:

```bash
ACTIVE_VENDOR=gemini
GOOGLE_API_KEY=your_google_api_key
FLOWBEAST_OUTPUT_DIR=./flowbeast/data/outputs
FLOWBEAST_VECTOR_DIR=./flowbeast/data/vectors
```

## First Run

```bash
python -m scripts.init_fp3
python main.py --topic "一个关于人工智能的短剧"
```

## Next Steps

- 📖 Read the [Architecture](architecture.md) docs
- 🔧 Check out [Tech Debt](tech-debt.md) for known issues
- 📚 Explore [ADRs](adrs/index.md) for architectural decisions
