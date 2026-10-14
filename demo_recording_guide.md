# FlowBeast Demo Recording Guide

## Setup

```bash
# Terminal 1: Start API server
uvicorn flowbeast.api.main:app --reload --port 8000

# Terminal 2: Start Streamlit UI
uv run streamlit run flowbeast/demo/app.py --server.port 8501
```

## Recording Script (1-3 minutes)

### 0:00 - Introduction (10s)
"FlowBeast is a Viral Prompt Compiler. Input a topic, and it produces a complete prompt package for AI video tools. The unique feature is viral structure transfer through GRAFT."

### 0:10 - Topic Input (20s)
1. Open browser to http://localhost:8501
2. Show the topic input field
3. Type or select a recommended topic (e.g., "AI Agent 取代白领")
4. Check "Use GRAFT" option
5. Click "Generate"

### 0:30 - Task Status (15s)
1. Show the polling progress bar
2. Highlight the current stage progression:
   - GRAFT_RETRIEVAL → GRAFT_APPLIED → GENERATION → SHOT_DIRECTION → AUDIO → EXPORT → COMPLETE

### 0:45 - Retrieved Viral Structure (30s)
1. Show the "Retrieved Viral Structure (GRAFT)" section
2. Highlight Hook Structure: type, timing, emotional payload
3. Highlight Conflict Pattern: type, escalation curve, reversal count
4. Show the source viral script

### 1:15 - Generated Script (30s)
1. Show the title and core hook
2. Scroll through the scenes
3. Point out how the GRAFT structure is visible in the generated content

### 1:45 - Audio (15s)
1. Play the episode audio
2. Show individual audio files per scene/dialogue

### 2:00 - Downloads (15s)
1. Show download buttons
2. Download prompt_package.json
3. Briefly show the JSON structure

### 2:15 - Conclusion (15s)
"This is how FlowBeast transfers viral narrative structures to new topics. The GRAFT operator extracts proven hook and conflict patterns, then applies them during generation."

## Key Evidence Points

1. **GRAFT vs Standard**: Run the same topic twice — once with GRAFT, once without. The scripts will have visibly different structures.
   - GRAFT: follows extracted hook/conflict patterns
   - Standard: follows default template patterns

2. **Structure Transfer**: The generated script's hook type and conflict engine match the extracted structure, not the original content.

3. **5 Evidence Runs**: All 5 runs in `flowbeast/data/outputs/evidence/` show consistent GRAFT application.

## Quick Demo (API-only, no UI)

```bash
# Submit task
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI Agent 取代白领", "use_graft": true}'

# Check status (poll)
curl http://localhost:8000/api/v1/tasks/{task_id}

# Download prompt package
curl http://localhost:8000/api/v1/download/prompt_package/{run_id} \
  -o prompt_package.json
```
