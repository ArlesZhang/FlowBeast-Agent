#!/bin/bash
# Start FlowBeast API server for Railway deployment

# Ensure we're in the project directory
cd "$(dirname "$0")"

# Activate virtual environment if not already active
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Start the FastAPI server
echo "🌊 Starting FlowBeast API server..."
uv run uvicorn flowbeast.api.main:app --host 0.0.0.0 --port ${PORT:-8000}
