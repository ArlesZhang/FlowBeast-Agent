"""
API: FastAPI server for FlowBeast.

Role: Web interface for topic-to-production-package generation.
Endpoints: POST /api/v1/generate, GET /api/v1/tasks/{task_id}, GET /health

Workflow: POST /api/v1/generate {topic} → background task → prompt_package.json + audio
"""

import sys
import json
import uuid
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from fastapi.responses import FileResponse
from loguru import logger
from pydantic import BaseModel

# Ensure project root is on sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# ==================== 初始化 ====================
app = FastAPI(title="FlowBeast", version="0.7.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==================== 任务状态存储 ====================
# In-memory task registry (JSON-backed for persistence)
TASKS_FILE = BASE_DIR / "flowbeast" / "data" / "runtime" / "tasks_state.json"
_task_state: dict = {}


def _load_tasks():
    global _task_state
    if TASKS_FILE.exists():
        try:
            _task_state = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
        except Exception:
            _task_state = {}


def _save_tasks():
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    TASKS_FILE.write_text(json.dumps(_task_state, ensure_ascii=False, indent=2), encoding="utf-8")


_load_tasks()


def _update_task(task_id: str, **kwargs):
    if task_id in _task_state:
        _task_state[task_id].update(kwargs)
        _task_state[task_id]["updated_at"] = datetime.now().isoformat()
        _save_tasks()


# ==================== Pydantic 模型 ====================
class GenerateRequest(BaseModel):
    topic: str


class GenerateResponse(BaseModel):
    task_id: str
    status: str
    message: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    current_stage: str
    progress: int
    topic: str
    result: Optional[dict] = None
    error: Optional[str] = None


# ==================== 路由 ====================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "FlowBeast Engine",
    }


@app.post("/api/v1/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())[:8]

    _task_state[task_id] = {
        "task_id": task_id,
        "status": "PENDING",
        "current_stage": "queued",
        "progress": 0,
        "topic": req.topic,
        "created_at": datetime.now().isoformat(),
        "result": None,
        "error": None,
    }
    _save_tasks()

    background_tasks.add_task(_run_generation, task_id, req.topic)

    return GenerateResponse(
        task_id=task_id,
        status="PENDING",
        message=f"Task {task_id} queued for topic: {req.topic}",
    )


@app.get("/api/v1/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    if task_id not in _task_state:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    task = _task_state[task_id]
    return TaskStatusResponse(
        task_id=task["task_id"],
        status=task["status"],
        current_stage=task["current_stage"],
        progress=task["progress"],
        topic=task["topic"],
        result=task.get("result"),
        error=task.get("error"),
    )


# ==================== 后台任务 ====================

def _run_generation(task_id: str, topic: str):
    """Background task: runs the full FlowBeast pipeline."""
    try:
        from flowbeast.drama.pipeline import run_full_pipeline

        _update_task(task_id, status="RUNNING", current_stage="GENERATION", progress=10)

        result = run_full_pipeline(topic)

        if result is None:
            _update_task(
                task_id,
                status="FAILED",
                current_stage="generation_failed",
                progress=0,
                error="Pipeline returned None (LLM or API failure)",
            )
            return

        _update_task(task_id, current_stage="SHOT_DIRECTION", progress=50)

        # Read outputs
        run_id = result["run_id"]
        script_path = result["script_path"]
        report_path = result["report_path"]
        audio_path = result["audio_path"]
        episode_audio = result.get("episode_audio_path")
        prompt_package_path = result["base_path"] / "prompt_package.json"

        _update_task(task_id, current_stage="AUDIO", progress=70)

        # Read generated script for UI display
        script_data = json.loads(script_path.read_text(encoding="utf-8"))
        report_data = json.loads(report_path.read_text(encoding="utf-8"))
        shot_list_path = result["base_path"] / "shot_list.json"
        shots_data = json.loads(shot_list_path.read_text(encoding="utf-8")) if shot_list_path.exists() else []

        _update_task(task_id, current_stage="EXPORT", progress=85)

        # Build result summary
        result_summary = {
            "run_id": run_id,
            "topic": topic,
            "title": script_data.get("title", ""),
            "core_hook": script_data.get("core_hook", ""),
            "genre": script_data.get("genre", ""),
            "scenes_count": len(script_data.get("scenes", [])),
            "shots_count": len(shots_data),
            "quality_score": report_data.get("quality", {}).get("score", 0),
            "quality_action": report_data.get("quality", {}).get("action", ""),
            "audio_files": result.get("audio_count", 0),
            "episode_audio_path": str(episode_audio) if episode_audio else None,
            "script_path": str(script_path),
            "report_path": str(report_path),
            "prompt_package_path": str(prompt_package_path),
            "scenes": script_data.get("scenes", [])[:3],  # First 3 for preview
        }

        _update_task(task_id, status="COMPLETE", current_stage="COMPLETE", progress=100, result=result_summary)

        logger.success(f"✅ Task {task_id} completed")

    except Exception as e:
        logger.error(f"❌ Task {task_id} failed: {e}")
        _update_task(
            task_id,
            status="FAILED",
            current_stage="error",
            progress=0,
            error=str(e),
        )


# ==================== 文件下载 ====================

@app.get("/api/v1/download/{file_type}/{run_id}")
async def download_file(file_type: str, run_id: str):
    """Download prompt package, audio, or report for a given run."""
    output_dir = BASE_DIR / "flowbeast" / "data" / "outputs" / run_id

    file_map = {
        "prompt_package": output_dir / "prompt_package.json",
        "script": output_dir / "script.json",
        "report": output_dir / "production_report.json",
        "episode_audio": output_dir / "episode_audio.mp3",
    }

    if file_type not in file_map:
        raise HTTPException(status_code=400, detail=f"Unknown file type: {file_type}")

    file_path = file_map[file_type]
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {file_path.name}")

    media_type = "audio/mpeg" if file_type == "episode_audio" else "application/json"
    return FileResponse(str(file_path), media_type=media_type, filename=file_path.name)
